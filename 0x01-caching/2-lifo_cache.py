#!/usr/bin/python3
'''Class LIFOCache'''
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    '''class LIFOCache that inherits from
    BaseCaching and is a caching system'''
    def __init__(self):
        '''instantiation'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is None or item is None:
            return
        if (
                key not in self.cache_data and
                len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS
        ):
            last_key, _ = self.cache_data.popitem()
            print("DISCARD: {}".format(last_key))
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        ''' return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
