#!/usr/bin/python3
'''Class FIFOCache'''
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    '''class FIFOCache that inherits from
    BaseCaching and is a caching system'''
    def __init__(self):
        '''instantiation'''
        super().__init__()

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is not None and item is not None:
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                first = next(iter(self.cache_data))
                del self.cache_data[first]
                print("DISCARD: {}".format(first))
            self.cache_data[key] = item

    def get(self, key):
        ''' return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data:
            return None
        else:
            return self.cache_data[key]
