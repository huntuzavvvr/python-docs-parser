from prettytable import PrettyTable, ALL
from pathlib import Path
import datetime as dt
import csv
import logging
from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, args):
    if args.table == "term":
        pretty_output(results)
    elif args.table == "file":
        file_output(results, args)
    else:
        default_output(results)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.add_rows((results[1:]))
    table.hrules = ALL
    table.sortby = table.field_names[1]
    print(table)


def file_output(results, args):
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    now = dt.datetime.now()
    filename = f"{args.table}_{now.strftime(DATETIME_FORMAT)}.csv"
    file_path = results_dir / filename
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f"Data saved in {results_dir}")


def default_output(results):
    for result in results:
        print(*result)
