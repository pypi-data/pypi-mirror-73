import unittest
from nose.tools import raises
from lru.lrucache import LRUCache

class LRUCacheTest(unittest.TestCase):
    def setUp(self):
        self.capacity = 10
        self.cache = LRUCache(self.capacity)

        for i in range(self.capacity):
            self.cache.set(1, int(i))

    def tearDown(self):
        self.cache = None

    @raises(KeyError)
    def test_get(self):
        self.cache.set(1)