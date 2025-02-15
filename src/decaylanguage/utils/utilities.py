# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/decaylanguage for details.

from typing import Any, Dict, Iterator, List, Pattern, Tuple, Union


def iter_flatten(iterable: Union[List[str], Tuple[str, ...]]) -> Iterator[str]:
    """
    Flatten nested tuples and lists
    """
    for e in iterable:
        if isinstance(e, (list, tuple)):
            yield from iter_flatten(e)
        else:
            yield e


def split(x: str) -> List[str]:
    """
    Break up a comma separated list, but respect curly brackets.

    For example:
    this, that { that { this, that } }
    would only break on the first comma, since the second is in a {} list
    """

    c = 0
    i = 0
    out = []
    while len(x) > 0:
        if i + 1 == len(x):
            out.append(x[: i + 1])
            return out
        elif x[i] == "," and c == 0:
            out.append(x[:i])
            x = x[i + 1 :]
            i = -1
        elif x[i] == "{":
            c += 1
        elif x[i] == "}":
            c -= 1
        i += 1
    return out


def filter_lines(
    matcher: Pattern[str], inp: List[str]
) -> Tuple[List[Dict[str, Union[str, Any]]], List[str]]:
    """
    Filter out lines into new variable if they match a regular expression
    """
    matches = (matcher.match(ln) for ln in inp)
    output = [match.groupdict() for match in matches if match is not None]
    new_inp = [ln for ln in inp if matcher.match(ln) is None]
    return output, new_inp
