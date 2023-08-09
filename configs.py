import argparse
import logging
from logging.handlers import RotatingFileHandler
from constants import BASE_DIR


def configure_parser(avalable_modes):
    parser = argparse.ArgumentParser(description="Python Docs Parser")
    parser.add_argument("mode", help="Operation mods", choices=avalable_modes)
    parser.add_argument("-c", "--clear", help="Clear cache", action="store_true")
    parser.add_argument("-t", "--table", help="Output in PrettyTable", choices=["term", "file"])
    return parser


def configure_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "parse.log"
    handler = RotatingFileHandler(filename=log_file, maxBytes=10**6, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s-%(message)s-%(levelname)s",
        datefmt="%d.%m.%y:%H%M%S",
        handlers=(handler, logging.StreamHandler())
    )