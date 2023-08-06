#!/usr/bin/env python

import logging
import argparse
import boto3
import dateutil
import importlib
import os
import sys
import time
from datetime import datetime, timezone
from base64 import b64encode
from enum import Enum

from typing import Dict, Tuple, NamedTuple, Optional, Callable


class IteratorType(Enum):
    TrimHorizon = "TRIM_HORIZON"
    AtTimestamp = "AT_TIMESTAMP"
    Latest = "LATEST"


class Message(NamedTuple):
    message_id: str
    body: str
    attributes: Optional[Dict]
    receipt_handle: str


Messages = Tuple[Message, ...]


MESSAGE_BATCH_SIZE = 1

logger = logging.getLogger("lambda_kinesis")


ShardIterator = str
KinesisRecords = Tuple[Dict, ...]


def get_records(
    kinesis_client, stream_name: str, shard_iterator: str
) -> Tuple[KinesisRecords, ShardIterator]:
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator)
    raw_records = records_response["Records"]
    records = tuple(
        {
            "kinesis": {
                "data": b64encode(raw_record["Data"]).decode("utf-8"),
                "partitionKey": raw_record["PartitionKey"],
                "approximateArrivalTimestamp": raw_record["ApproximateArrivalTimestamp"],
            },
            "eventSource": "aws:kinesis",
            "eventName": "aws:kinesis:record",
        }
        for raw_record in raw_records
    )

    next_shard_iterator = records_response["NextShardIterator"]

    return records, next_shard_iterator


def format_kinesis_timestamp(dt: datetime):
    """
    Convert a datetime to a Kinesis supported timestamp value: ISO format with
    milliseconds percision and timezone info.

    Example: 2020-06-26T15:00:00.000-00:00
    """
    return dt.replace(tzinfo=timezone.utc).isoformat(timespec="milliseconds")


def run_handler_on_stream_records(
    stream_name: str,
    shard_iterator_type: IteratorType,
    handler: Callable,
    wait_seconds: int,
    *_,
    timestamp: Optional[datetime] = None,
    shard_id: Optional[str] = None,
    kinesis_client=None,
):
    logger.info("Starting to consume records from %s", stream_name)
    if timestamp:
        logger.debug("AT_TIMESTAMP %s", format_kinesis_timestamp(timestamp))

    kinesis_client = kinesis_client or boto3.client("kinesis")

    shard_id = (
        kinesis_client.list_shards(StreamName=stream_name, MaxResults=1)["Shards"][0]["ShardId"]
        if not shard_id
        else shard_id
    )

    logger.info("Consuming from shard %s", shard_id)

    timestamp_args = {"Timestamp": format_kinesis_timestamp(timestamp)} if timestamp else {}
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType=shard_iterator_type.value,
        **timestamp_args,
    )["ShardIterator"]

    while True:
        records, shard_iterator = get_records(kinesis_client, stream_name, shard_iterator)

        logger.info("Invoking lambda handler with %d records", len(records))

        event = {"Records": records}
        handler(event, None)

        time.sleep(wait_seconds)


def setup_logging():
    logging.getLogger("botocore").setLevel("WARNING")
    logging.getLogger("urllib3").setLevel("WARNING")
    logging.basicConfig(format="%(asctime)s %(name)s - %(message)s", level=logging.INFO)


def run_from_cli():
    sys.path.append(os.getcwd())
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Run a lambda handler locally on kinesis stream records."
    )
    parser.add_argument("-s", "--stream", help="Kinesis stream name", required=True)
    parser.add_argument(
        "--shard-id", help="Shard ID to consume from, defaults to the first in the stream."
    )
    parser.add_argument(
        "-p",
        "--handler",
        help="Path to the lambda handler function, for example: 'path.to.function'",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--iterator-type",
        help="Shard iterator type",
        default="TRIM_HORIZON",
        choices=[t.value for t in IteratorType],
    )
    parser.add_argument("-w", "--wait", help="Seconds to wait between reads", type=int, default=5)

    parser.add_argument(
        "-t",
        "--timestamp",
        help="""
        Filter events from timestamp using AT_TIMESTAMP iterator type.
        Treated as UTC and ignores any timezones in the timestamp.
        Examples (anything supported by dateparser):
            2020-06-26
            2020.6.26 10:22:10.55
        """,
        default=None,
    )

    args = parser.parse_args()

    iterator_type = IteratorType.AtTimestamp if args.timestamp else IteratorType(args.iterator_type)

    if iterator_type == IteratorType.AtTimestamp and not args.timestamp:
        print("Error: Timestamp must be specified for iterator type AT_TIMESTAMP")
        return

    try:
        timestamp = dateutil.parser.parse(args.timestamp) if args.timestamp else None
    except ValueError:
        print(f"Error: Could not parse timestamp '{args.timestamp}'")
        return

    handler_path = args.handler.replace("/", ".").split(".")
    module_path, handler_name = ".".join(handler_path[:-1]), handler_path[-1]

    module = importlib.import_module(module_path)
    handler = getattr(module, handler_name, None)

    if not handler:
        raise ValueError(f"Handler {args.handler} does not exist")

    run_handler_on_stream_records(
        stream_name=args.stream,
        shard_iterator_type=iterator_type,
        shard_id=args.shard_id,
        handler=handler,
        wait_seconds=args.wait,
        timestamp=timestamp,
    )


if __name__ == "__main__":
    run_from_cli()
