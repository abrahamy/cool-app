import argparse
import pathlib

from cool_app.consumer import start_consumer
from cool_app.producer import start_producer


def main():
    parser = argparse.ArgumentParser(
        prog="cool_app", description="A simple message processing app"
    )
    parser.set_defaults(func=lambda args: parser.print_help())

    subparsers = parser.add_subparsers(title="Commands")
    consumer = subparsers.add_parser("consumer", description="Start the consumer")
    consumer.set_defaults(func=start_consumer)

    producer = subparsers.add_parser("producer", description="Start the producer")
    producer.add_argument(
        "csv_file", type=pathlib.Path, help="The path to the csv file to process"
    )
    producer.set_defaults(func=start_producer)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
