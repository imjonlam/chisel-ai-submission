#!/usr/bin/python3.6
#################################################
#             CHISEL AI - TAKE-HOME             #
#         LRU CACHE IMPLEMENTATION CLI          #
#                 Jonathan Lam                  #
#            jonathanlam.1994@gmail             #
#                (647)-992-2698                 #
#################################################

import os
import sys
import signal
from LRUCache import LRUCache

def signal_handler(sig, frame):
  '''Handle CTRL+C interrupt'''
  print('\nBye bye!')
  sys.exit(0)

def get_docstring():
  '''
  Welcome to the LRU Cache Test Panel.
  The following options are available:

  1. Create a new cache:                  create
  2. Print current cache:                 show
  3. Put a key,value pair into the cache: put
  4. Delete a key from the cache:         delete
  5. Reset the cache:                     reset
  6. exit:                                quit
  '''
  print(get_docstring.__doc__)

def is_cache_none(cache: LRUCache) -> bool:
  '''
  Check if cache is empty

  Args:
    cache: LRUCache instance

  Returns:
    A boolean if cache exists or not
  '''
  if cache is None:
    print('ERROR: cache has not been created. Please create first.')
    return cache is None

def create(cache) -> LRUCache:
  '''
  Creates a new cache

  Args:
    cache: LRUCache instance

  Returns:
    A new LRUCache
  '''
  # check if cache exists, wipe if confirmed
  if cache is not None:
    confirm = input('WARNING: cache is not empty, confirm reset (YES|NO): ')
    if confirm.upper() != 'YES':
      print('ERROR: user denied destroying existing cache.')
      return cache
    else:
      cache = None

  # request cache capacity
  try:
    max_size = int(input('Enter maximum capacity: '))
  except ValueError:
    print('ERROR: entered capacity is not an integer.')
    return

  # try to make cache; otherwise retry
  try:
    cache = LRUCache(max_size)
    print(f'Cache successfully created with max. capacity: {max_size}')
    return cache
  except ValueError as e:
    print(e)
    return

def get(cache: LRUCache):
  '''
  Retrieves an item from the cache

  Args:
    cache: LRUCache instance
  '''
  # check if cache exists, if not no-op
  if is_cache_none(cache): return

  # retrieve value
  key = input('Enter key: ').strip()
  try:
    val = cache.get(key)
    print(f'The value is: {val}')
  except KeyError as e:
    print(e)

def put(cache: LRUCache):
  '''
  Inserts a new entry into the cache

  Args:
    cache: LRUCache instance
  '''
  # check if cache exists, if not no-op
  if is_cache_none(cache): return
  
  # insert key, value into cache
  key, val = input('Enter key: ').strip(), input('Enter value: ')
  cache.put(key, val)
  print(f'successfully inserted [{key}: {val}] into the cache.')

def delete(cache):
  '''
  Deletes a key from the cache; no-op if DNE

  Args:
    cache: LRUCache instance
  '''
  # check if cache exists, if not no-op
  if is_cache_none(cache): return

  key = input('Enter key to delete: ').strip()
  cache.delete(key)
  print(f'successfully deleted {key} from the cache.')

def reset(cache: LRUCache):
  '''
  Deletes a key from the cache; no-op if DNE

  Args:
    cache: LRUCache instance
  '''
  # check if cache exists, if not no-op
  if is_cache_none(cache): return

  cache.reset()
  print('successfully resetted the cache')

def print_cache(cache: LRUCache):
  '''
  Prints to screen current cache state

  Args:
    cache: LRUCache instance
  '''
  # check if cache exists, if not no-op
  if is_cache_none(cache): return

  stream = cache.head
  print('CACHE HEAD -> ', end='')
  while (stream is not None):
    print(f'[{stream.key}, {stream.val}]', end='')
    stream = stream.next
    if stream is not None: print(' -> ', end='')

  print(' <- TAIL')

def run():
  '''Run the CLI Test Panel'''
  # print out instructions
  get_docstring()

  # trap signal
  signal.signal(signal.SIGINT, signal_handler)

  # begin cli
  cache = None
  command = input('Enter a command: ')
  while (command != 'exit'):
    if command == 'create':
      cache = create(cache)
    elif command == 'show':
      print_cache(cache)
    elif command == 'get':
      get(cache)
    elif command == 'put':
      put(cache)
    elif command == 'delete':
      delete(cache)
    elif command == 'reset':
      reset(cache)
    elif command == 'quit':
      print('Bye bye!')
      sys.exit(0)
    else:
      print('Invalid command received.')
    
    # wait for next command
    command = input('\nEnter next command: ')

if __name__ == "__main__":
  try:
    run()
  except Exception as e:
    print(e)