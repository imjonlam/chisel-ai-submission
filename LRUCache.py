#!/usr/bin/python3.6
#################################################
#             CHISEL AI - TAKE-HOME             #
#            LRU CACHE IMPLEMENTATION           #
#                 Jonathan Lam                  #
#            jonathanlam.1994@gmail             #
#                (647)-992-2698                 #
#################################################

# Assumptions:
# 1) the maximum cache size must be greater than or equal to 1
# 2) the key must exist when calling get
# 3) you must be able to put the value of a key, overwrite if exists
# 4) deleting a key that doesn't exist is a no-op

class KeyExistsError(Exception):
  '''Custom Exception class for handling existing keys in dictionary'''
  def __init__(self, message):
    '''Initialize KeyExistsError class'''
    super().__init__(message)

class Node:
  ''' 
  A Node representing a singular cache item 
  
  Attributes:
    key: unique identifier of node
    val: a node's value
    prev: reference to previous node
    next: reference to next node
  '''
  def __init__(self, key=None, val=None):
    '''Initialize Node class'''
    self.key = key
    self.val = val
    self.prev, self.next = None, None

class LRUCache:
  ''' 
  Construction of a Least-Recently Used (LRU) Cache
  
  Attributes:
    count: current number of items stored
    items: dictionary of key,value pairs
    capacity: integer value of the cache's maximum sie
    head: reference to the head Node
    tail: reference to the tail Node
  '''
  def __init__(self, max_size: int):
    '''Initialize LRUCache class'''
    if max_size < 1:
      raise ValueError(f'ERROR: max items cannot be less than 0, given {max_size}.')

    self.count = 0
    self.items = {}
    self.capacity = max_size
    self.head, self.tail = None, None

  def get(self, key):
    '''
    Get the value by key in the cache

    Args:
      key: represents the cache item to retrieve the value from

    Returns:
      The corresponding value of the key

    Raises:
      KeyError: An error occured where the key does not exist in the dictionary
    '''
    # check if key is available
    node = self.items.get(key, None)
    if node is None:
      raise KeyError(f'ERROR: the key {key} does not exist.')

    # if node is at the front; return
    if node.prev == None:
      return node.val
    else:
      node.prev.next = node.next

    # if node is somewhere in the middle / end
    if node.next != None:
      node.next.prev = node.prev
    else:
      self.tail = node.prev

    # position the node to the front of the list
    node.next = self.head
    self.head.prev = node
    node.prev = None
    self.head = node

    return node.val

  def put(self, key, val):
    '''
    Puts the value by key into the cache at the front-most position

    Args:
      key: represents the cache item to retrieve the value from
      val: corresponding value of key
    '''
    # if the key already exists, simply update its value
    node = self.items.get(key, None)
    if node is not None:
      node.key, node.val = key, val
      self.get(key)
      return

    # check if cache overflow will occur
    if self.count + 1 > self.capacity:
      self.__delete_last()

    # otherwise, we create a new node; add to front
    node = Node(key, val)

    # if the LinkedList is empty, simply add
    if self.head is None:
      self.head = node
      self.tail = node
    else:
      node.next = self.head
      self.head.prev = node
      self.head = node

    self.items[key] = node
    self.count += 1

  def delete(self, key):
    '''
    Deletes the cache item associated with key

    Args:
      key: represents the cache item to retrieve the value from

    Raises:
      KeyError: An error occured where the key does not exist in the dictionary
    '''
    # check if key exists
    node = self.items.get(key, None)
    if node is None:
      return

    # if there is only one item, simply reset
    if self.count == 1:
      self.reset()
      return

    # remove node and repoint references
    if node.prev is None:
      self.head = node.next
      self.head.prev = None
    else:
      node.prev.next = node.next

    if node.next is not None:
      node.next.prev = node.prev
    else:
      self.tail = self.tail.prev
      self.tail.next = None

    # update items
    self.items.pop(key)
    self.count -= 1
  
    node = None

  def reset(self):
    '''Resets the cache'''
    self.items.clear()
    self.count = 0

    self.head, self.tail = None, None

  def __delete_last(self):
    '''Deletes the least used item in the cache'''
    # get last node in the cache (lru)
    node = self.tail

    # if there is only one item, simply reset
    if self.count == 1:
      self.reset()
      return

    # remove
    self.tail = self.tail.prev
    self.tail.next = None

    # update items
    self.items.pop(node.key)
    self.count -= 1    

    node = None