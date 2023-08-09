import argparse


def configure_parser(avalable_modes):
    parser = argparse.ArgumentParser(description="Python Docs Parser")
    parser.add_argument("mode", help="Operation mods", choices=avalable_modes)
    parser.add_argument("-c", "--clear", help="Clear cache", action="store_true")
    parser.add_argument("-t", "--table", help="Output in PrettyTable format", action="store_true")
    return parser