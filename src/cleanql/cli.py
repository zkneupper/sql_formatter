#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Python standard library
# import pathlib
import functools
import sys

# External packages
import click

# Internal modules
# import formatter
import cleanql.formatter as formatter
import cleanql.preprocess_paths as preprocess_paths


out = functools.partial(click.secho, bold=True, err=True)
err = functools.partial(click.secho, fg="red", err=True)


def read_file(filepath):
    with open(filepath, "r") as file:
        text = file.read()
    return text


def write_file(filepath, text):
    with open(filepath, "w") as file:
        file.write(text)


# functools.partial


def bold_color(message, color="red"):
    color_code_dict = {
        "red": "31m",
        "green": "32m",
        "yellow": "33m",
    }
    color_code = color_code_dict[color]
    message_red_bold = f"\x1b[1;{color_code}{message}\x1b[0m"
    return message_red_bold


def print_error(message):
    """Print with bold red text for failure messages to stderr"""
    # message_red_bold = f"\x1b[1;31m{message}\x1b[0m"
    message_red_bold = bold_color(message, color="red")
    print(message_red_bold, file=sys.stderr, flush=True)


def check_filename_extension(filename):
    if not filename.suffix.lower() == ".sql":
        message = f"Invalid file type. `{filename}` is not a `.sql` file."
        print_error(message)
        sys.exit(1)


def check_filename_exists(filename):
    if not filename.exists():
        message = f"File `{filename}` not found."
        print_error(message)
        sys.exit(1)


# Handle multiple files
# .
# or
# no arg

flavors = [
    "COMMON",
    "HQL",
    # "IMPALA",
    "ORACLE",
    "POSTGRESQL",
    # "SPARK",
]


@click.command()
@click.argument("paths", nargs=-1)
@click.option(
    "--flavor",
    "-f",
    type=click.Choice(flavors, case_sensitive=False),
    default="COMMON",
    help="Specify the favor of SQL syntax.",
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Print verbose output.",
)
def cli(paths, flavor, verbose):
    """The uncompromising SQL formatter."""

    # paths will be a tuple, because nargs=-1
    # Convert tuple to list ; list of pathlib paths
    paths = preprocess_paths._preprocess_paths(paths)

    reformatted = "reformatted"
    unchanged = "left unchanged"
    failed = "failed to reformat"

    change_count = 0
    same_count = 0
    failure_count = 0

    for filepath in paths:

        check_filename_extension(filepath)
        check_filename_exists(filepath)

        sql = read_file(filepath)
        sql_output = formatter.format_sql(sql, sql_keywords=None)

        if sql == sql_output:
            same_count += 1
            # print(f"Unchanged: {filepath}")
        else:
            change_count += 1

            write_file(filepath, sql_output)

            # message = "Formatted: "
            # message = bold_color(message, color="green")
            # message += str(filepath)
            # print(message, flush=True)

    out("All done! ✨ 🍰 ✨")

    report = list()

    if change_count:
        s = "s" if change_count > 1 else ""
        report.append(click.style(f"{change_count} file{s} {reformatted}", bold=True))

    if same_count:
        s = "s" if same_count > 1 else ""
        report.append(f"{same_count} file{s} {unchanged}")

    report = ", ".join(report) + "."
    click.secho(str(report))


if __name__ == "__main__":
    cli()
