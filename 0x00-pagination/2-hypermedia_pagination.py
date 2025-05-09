#!/usr/bin/env python3
'''Function index_range'''
from typing import Tuple, List, Dict
import csv
import math


def index_range(page: int, page_size: int) -> Tuple:
    '''Function that  returns a tuple of size two
    containing a start index and an end index'''
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''return the desired page'''
        assert isinstance(page, int) and page >= 0
        assert isinstance(page_size, int) and page_size >= 0
        start, end = index_range(page, page_size)
        dataset_list = self.dataset()
        return dataset_list[start: end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        total_items = len(self.dataset())
        total_pages = (total_items + page_size - 1) // page_size
        if page > total_pages:
            page_size = 0
        if (page + 1 < total_pages):
            next_page = page + 1
        else:
            next_page = None
        if (page - 1 > 0):
            prev_page = page - 1
        else:
            prev_page = None
        return {
            'page_size': page_size,
            'page': page,
            'data': self.get_page(page, page_size),
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
