# 简易版lru
import collections


class LRUCache:
    def __init__(self, capacity=9):
        self.list = None
        self.list = collections.OrderedDict()
        self.capacity = capacity
        
    def get(self, key):
        if key in self.list:
            val = self.list[key]
            self.list.move_to_end(key)
            return val
        return -1

    def put(self, key, value):
        if key in self.list:
            del self.list[key]
        self.list[key] = value
        if len(self.list) > self.capacity:
            self.list.popitem(last=False) 
        return self.list[key]

    def __call__(self, func):
        def _inner(*args, **kwargs):
            if args[0] in self.list:
              return self.list[args[0]]
            else:
              res = func(*args, **kwargs)
              self.put(args[0],res)
              return res
        return _inner
    