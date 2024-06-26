#!/usr/bin/env python3
'''Annotating given function params and returning values with the
appropriate types'''
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''calculates the lengths of the given params'''
    return [(i, len(i)) for i in lst]
