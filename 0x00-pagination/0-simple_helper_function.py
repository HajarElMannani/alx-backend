#!/usr/bin/env python3
'''Function index_range'''
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    '''Function that  returns a tuple of size two
    containing a start index and an end index'''
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
