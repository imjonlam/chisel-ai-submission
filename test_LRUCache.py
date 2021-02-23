#!/usr/bin/python3.6
#################################################
#             CHISEL AI - TAKE-HOME             #
#         LRU CACHE IMPLEMENTATION PYTESTS      #
#                 Jonathan Lam                  #
#            jonathanlam.1994@gmail             #
#                (647)-992-2698                 #
#################################################

import pytest
from LRUCache import LRUCache

@pytest.fixture
def supply_sample_cache():
  # initialize sample cache with capacity = 5
  cache = LRUCache(6)

  # insert sample data
  cache.put('one', 1)
  cache.put('two', 2)
  cache.put('three', 3)
  cache.put('four', 4)
  cache.put('five', 5)

  return cache

@pytest.fixture
def supply_empty_cache():
  #initialize sample cache with capacity = 1
  cache = LRUCache(1)
  return cache

@pytest.fixture
def supply_one_item_cache():
  #initialize sample one item cache with capacity = 1
  cache = LRUCache(1)
  cache.put('one', 1)
  return cache

##########################
# Exceptions Testing     #
##########################

def test_negative_capacity_initialization():
  '''EXCEPTIONS: the maximum cache size must be greater than or equal to 0'''
  with pytest.raises(ValueError):
    LRUCache(0)

def test_getting_unknown_key(supply_sample_cache):
  '''EXCEPTIONS: the key must exist when trying to retrieve'''
  with pytest.raises(KeyError):
    supply_sample_cache.get('UNKNOWN_KEY')

##########################
# Testing for GET        #
##########################

def test_get_bring_to_front(supply_sample_cache):
  '''GET: retrieving a key should bring it to the front'''
  val = supply_sample_cache.get('three')
  assert(val == 3)
  assert(supply_sample_cache.head.val == val)

def test_get_most_used(supply_sample_cache):
  '''GET: retrieving most-used node; should not change cache order'''
  head_val = supply_sample_cache.head.val

  val = supply_sample_cache.get('five')
  assert(head_val == val)


def test_get_least_used(supply_sample_cache):
  '''GET: retrieving least-used item, new tail should become second last'''
  head_val = supply_sample_cache.head.val
  tail_val = supply_sample_cache.tail.val
  tail_prev_val = supply_sample_cache.tail.prev.val

  supply_sample_cache.get('one')
  assert(tail_val == supply_sample_cache.head.val)
  assert(supply_sample_cache.tail.val == tail_prev_val)
  assert(supply_sample_cache.head.next.val == head_val)

##########################
# Testing for PUT        #
##########################

def test_put_into_empty_cache(supply_empty_cache):
  '''PUT: put new node into empty cache'''
  assert(supply_empty_cache.count == 0)

  supply_empty_cache.put('one', 1)

  assert(supply_empty_cache.count == 1)
  assert(supply_empty_cache.head.val == 1)
  assert(supply_empty_cache.head == supply_empty_cache.tail)
  assert(supply_empty_cache.items.get('one', None) is not None)

def test_put_to_front(supply_sample_cache):
  '''PUT: put new node into existing cache; update most used'''
  head_val = supply_sample_cache.head.val
  tail_val = supply_sample_cache.tail.val

  supply_sample_cache.put('six', 6)  
  assert(supply_sample_cache.head.val == 6)
  assert(supply_sample_cache.head.next.val == head_val)
  assert(supply_sample_cache.tail.val == tail_val)
  assert(supply_sample_cache.items.get('six', None) is not None)

def test_put_overflow1(supply_sample_cache):
  '''PUT: test overflow of cache of capacity - removes least-used node before new put'''
  supply_sample_cache.put('six', 6)
  initial_count = supply_sample_cache.count
  tail_prev_val = supply_sample_cache.tail.prev.val

  supply_sample_cache.put('seven', 7)
  assert(initial_count == supply_sample_cache.count)
  assert(supply_sample_cache.head.val == 7)
  assert(supply_sample_cache.tail.val == tail_prev_val)
  assert(supply_sample_cache.items.get('one', None) is None)

def test_put_overflow2(supply_one_item_cache):
  '''PUT: test overflow of a cache with capacity of 1'''
  supply_one_item_cache.put('two', 2)
  assert(supply_one_item_cache.count == 1)
  assert(supply_one_item_cache.head == supply_one_item_cache.tail)
  assert(supply_one_item_cache.items.get('one', None) is None)
  assert(supply_one_item_cache.items.get('two', None) is not None)

def test_put_existing_key1(supply_sample_cache):
  '''PUT: inserting an existing key - updates value, puts to front'''
  initial_count = supply_sample_cache.count

  supply_sample_cache.put('two', 20)
  assert(supply_sample_cache.count == initial_count)
  assert(supply_sample_cache.head.key == 'two')
  assert(supply_sample_cache.head.val == 20)

def test_put_existing_key2(supply_sample_cache):
  '''PUT: inserting an existing key corresponding to least used item - updates value, puts to front'''
  initial_count = supply_sample_cache.count
  tail_prev_val = supply_sample_cache.tail.prev

  supply_sample_cache.put('one', 10)
  assert(supply_sample_cache.count == initial_count)
  assert(supply_sample_cache.head.key == 'one')
  assert(supply_sample_cache.head.val == 10)
  assert(supply_sample_cache.tail.val == tail_prev_val.val)

def test_put_existing_key3(supply_sample_cache):
  '''PUT: inserting an existing key corresponding to most used item - updates value'''
  initial_count = supply_sample_cache.count
  initial_head = supply_sample_cache.head

  supply_sample_cache.put('five', 50)
  assert(supply_sample_cache.count == initial_count)
  assert(supply_sample_cache.head.key == initial_head.key)
  assert(supply_sample_cache.head.val == 50)

# ##########################
# # Testing for DELETE     #
# ##########################

def test_delete_head(supply_sample_cache):
  '''DELETE: delete head node, test count decrement'''
  initial_count = supply_sample_cache.count
  next_val = supply_sample_cache.head.next.val
  supply_sample_cache.delete('five')
  assert(supply_sample_cache.head.val == next_val)
  assert(supply_sample_cache.count == initial_count - 1)
  assert(supply_sample_cache.items.get('five', None) is None)

def test_delete_tail(supply_sample_cache):
  '''DELETE: delete from tail, new least used should be previously second last'''
  tail_prev_val = supply_sample_cache.tail.prev.val
  supply_sample_cache.delete('one')
  assert(supply_sample_cache.tail.val == tail_prev_val)
  assert(supply_sample_cache.items.get('one', None) is None)

def test_delete_only_remaining(supply_one_item_cache):
  '''DELETE: delete the last item in cache; resets'''
  supply_one_item_cache.delete('one')
  assert(supply_one_item_cache.head is None)
  assert(supply_one_item_cache.tail is None)
  assert(supply_one_item_cache.count == 0)
  assert(not supply_one_item_cache.items)

def test_delete_from_empty_cache(supply_empty_cache):
  '''DELETE: attempt to delete a key from an empty cache'''
  supply_empty_cache.delete('unknown_key')
  assert(supply_empty_cache.head is None)
  assert(supply_empty_cache.tail is None)
  assert(supply_empty_cache.count == 0)
  assert(not supply_empty_cache.items)

def test_delete_unknown_key(supply_one_item_cache):
  '''DELETE: attempt to delete a key from an non-empty cache'''
  supply_one_item_cache.delete('unknown_key')
  assert(supply_one_item_cache.count == 1)
  assert(supply_one_item_cache.head == supply_one_item_cache.tail)
  assert(supply_one_item_cache.items.get('one', None) is not None)

# ##########################
# # Testing for RESET      #
# ##########################

def test_reset(supply_sample_cache):
  '''RESET: test resetting cache'''
  supply_sample_cache.reset()
  assert(supply_sample_cache.head is None)
  assert(supply_sample_cache.tail is None)
  assert(supply_sample_cache.count == 0)
  assert(not supply_sample_cache.items)