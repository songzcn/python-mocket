# coding=utf-8
import redis
from unittest import TestCase
from mocket.mockredis import Entry
from mocket.registry import mocketize


class RedisEntryTestCase(TestCase):
    def mocketize_setup(self):
        self.rclient = redis.StrictRedis()
        #self.rclient.flushall()

    @mocketize
    def test_truesendall_set(self):
        self.rclient.flushall()
        self.assertTrue(self.rclient.set('mocket', 'is awesome!'))

    @mocketize
    def test_sendall_set(self):
        Entry.single_register('SET mocket "is awesome!"', '+OK')
        self.assertTrue(self.rclient.set('mocket', 'is awesome!'))

    @mocketize
    def test_truesendall_incr(self):
        self.rclient.flushall()
        self.assertEqual(self.rclient.incr('counter'), 1)
        self.assertEqual(self.rclient.incr('counter'), 2)
        self.assertEqual(self.rclient.incr('counter'), 3)

    @mocketize
    def _test_sendall_incr(self):
        Entry.multi_register('INCRBY counter 1', (Entry.redis_int(1), Entry.redis_int(2), Entry.redis_int(3)))

        self.assertEqual(self.rclient.incr('counter'), 1)
        self.assertEqual(self.rclient.incr('counter'), 2)
        self.assertEqual(self.rclient.incr('counter'), 3)

    @mocketize
    def test_truesendall_hm(self):
        self.rclient.flushall()
        h = {'f1': 'one', 'f2': 'two'}
        self.assertTrue(self.rclient.hmset('hash', h))
        self.assertEqual(self.rclient.hgetall('hash'), h)

    @mocketize
    def test_sendall_hgetall(self):
        h = {'f1': 'one', 'f2': 'two'}
        Entry.single_register('HGETALL hash', Entry.redis_map({'f1': 'one', 'f2': 'two'}))

        self.assertEqual(self.rclient.hgetall('hash'), h)