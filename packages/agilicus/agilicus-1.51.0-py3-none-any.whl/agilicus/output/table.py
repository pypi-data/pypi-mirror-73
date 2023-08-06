import datetime
import operator

from dataclasses import dataclass

from prettytable import PrettyTable


def format_date(date_input):
    return date_input.strftime("%Y-%m-%d %H:%M:%S %z (%Z)")


def date_else_identity(column, input_obj):
    if isinstance(input_obj, datetime.datetime):
        return format_date(input_obj)
    return input_obj


@dataclass
class OutputColumn:
    in_name: str
    out_name: str
    format_fn = date_else_identity


def column(name):
    return OutputColumn(in_name=name, out_name=name)


def mapped_column(in_name, out_name):
    return OutputColumn(in_name=in_name, out_name=out_name)


def format_table(records, columns, getter=operator.attrgetter):
    table = PrettyTable([column.out_name for column in columns])
    for record in records:
        row = []
        for column in columns:
            in_value = getter(column.in_name)(record)
            out_value = "---"
            if in_value is not None:
                out_value = column.format_fn(in_value)
            row.append(out_value)

        table.add_row(row)
    table.align = "l"
    return table
