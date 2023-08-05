import argparse
import json
import logging

from multiprocessing import cpu_count
from pathlib import Path
from skelate import skeleton


def cli():
    """ Return an `argparse.ArgumentParser` providing a basic CLI for `skelate`.
    """

    parser = argparse.ArgumentParser(
        description="Create a directory from a skeleton, with templating."
    )

    parser.add_argument(
        "--vars",
        default=None,
        help="Path to JSON file containing variables for templates."
    )

    parser.add_argument(
        "-e", "--extra-vars",
        default=[], action="append", type=str,
        help=str(
            "One or more name=value pairs for templating. "
            "The value can be a JSON object."
        )
    )

    parser.add_argument(
        "-t", "--template-extensions",
        default=["j2"], type=str, action="append",
        help="Extension of template files to expand (default: %(default)s)"
    )

    parser.add_argument(
        "-w", "--workers",
        default=4*cpu_count(), type=int,
        help="Number of workers to use (default: %(default)s)"
    )

    parser.add_argument(
        "-V", "--verbose",
        default=False, action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "-D", "--debug",
        default=False, action="store_true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "skeleton",
        metavar="SKEL", type=Path,
        help="Path to skeleton directory"
    )

    parser.add_argument(
        "target",
        metavar="TARGET", type=Path,
        help="Path to target directory"
    )

    return parser


def get_console_logger(params):
    logger = logging.getLogger("skelate")

    loglevel = logging.WARNING
    if params.get("verbose") is True:
        loglevel = logging.INFO

    if params.get("debug") is True:
        loglevel = logging.DEBUG

    logger.setLevel(loglevel)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s][%(levelname)s] %(message)s",
            datefmt="%Y%m%dT%H:%M:%S%z"
        )
    )
    logger.addHandler(ch)

    return logger


def parse_extra_vars(extra_vars=[]):
    variables = dict()

    for extra_var in extra_vars:
        var = extra_var.split("=", 1)

        try:
            variables[var[0]] = json.loads(var[1])
        except json.decoder.JSONDecodeError:
            variables[var[0]] = str(var[1])

    return variables


def main():

    params = cli().parse_args()
    logger = get_console_logger(vars(params))
    logger.debug("Starting skelate.")
    variables = dict()

    if params.vars:
        variables = json.load(open(params.vars, 'rb'))

    variables.update(parse_extra_vars(params.extra_vars))

    skel = skeleton.Skeleton(
        params.skeleton,
        workers=params.workers,
        variables=variables,
        template_extensions=params.template_extensions
    )
    skel.create(params.target, variables=variables)
