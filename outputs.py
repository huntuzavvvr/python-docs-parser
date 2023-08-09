from prettytable import PrettyTable, ALL

def control_output(results, args):
    if args.table:
        pretty_output(results)
    else:
        default_output(results)



def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.add_rows((results[1:]))
    table.hrules = ALL
    table.sortby = table.field_names[1]
    print(table)

def default_output(results):
    for result in results:
        print(*result)
