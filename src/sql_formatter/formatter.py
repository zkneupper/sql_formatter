#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Python standard library
import pathlib
import re

# External packages
import sqlparse


def remove_nones(iterable):
    return (x for x in iterable if x is not None)


def remove_empty_strings(iterable):
    return (x for x in iterable if x != "")


def split_sql(sql):
    pattern = "(\-\-.+\n)|(\".+\")|('.+')|(\$\{.+\})|(\W)"
    tokens = re.split(pattern, sql)
    tokens = remove_nones(tokens)
    tokens = remove_empty_strings(tokens)
    tokens = list(tokens)
    return tokens


def is_keyword(string, sql_keywords):
    return string.lower() in sql_keywords


def capitalize_keywords(string, sql_keywords):
    if is_keyword(string, sql_keywords):
        return string.upper()
    else:
        return string


def preserve_case(string):
    pattern = "(\-\-.+\n)|(\".+\")|('.+')"  # |(\$\{.+\})|(\W)"
    return bool(re.fullmatch(pattern, string))


def make_lower_case(string, sql_keywords):
    if preserve_case(string):
        return string
    elif is_keyword(string, sql_keywords):
        return string
    else:
        return string.lower()


def format_indentation(sql):

    format_kwargs = {
        "keyword_case": "upper",
        "identifier_case": "lower",
        "strip_comments": False,
        "use_space_around_operators": True,
        "comma_first": False,
        "reindent": True,
        "indent_width": 4,
        "indent_tabs": False,
        "indent_columns": True,
        "strip_whitespace": True,
    }

    sql_output = sql

    # Formatting sometimes doesn't work if you only run it once
    for _ in range(5):
        sql_output = sqlparse.format(sql_output, **format_kwargs)

    return sql_output


def remove_trailing_whitespace(string):
    string_output = (x.rstrip() for x in string.split("\n"))
    string_output = "\n".join(string_output)
    return string_output


def format_sql(sql):

    sql_output = sql
    sql_output = format_indentation(sql_output)
    sql_output = remove_trailing_whitespace(sql_output)
    return sql_output
