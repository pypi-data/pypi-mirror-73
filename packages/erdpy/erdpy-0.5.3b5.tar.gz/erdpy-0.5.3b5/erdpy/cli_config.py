import logging

from erdpy import dependencies, errors

logger = logging.getLogger("cli.config")


def setup_parser(subparsers):
    parser = subparsers.add_parser("config")
    subparsers = parser.add_subparsers()
