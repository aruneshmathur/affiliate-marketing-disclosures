#!/usr/bin/python

import requests
import json
import dataset
import time
import multiprocessing as mp
import sys
import logging
import traceback
import random
import itertools
import pandas as pd
import re
from itertools import izip_longest


def grouper(n, iterable, fillvalue = None):
  args = [iter(iterable)] * n
  return izip_longest(fillvalue = fillvalue, *args)


def compile_urls(pins_list):
  result_list = []
  pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

  for pin in pins_list:

    if (pin is None):
      continue

    if (pin['link'] is not None and pin['link'] != ''):
      res = {}
      res['pinId'] = pin['id']
      res['url'] = pin['link']
      res['origin'] = 'link'
      result_list.append(res)

    if (pin['trackedLink'] is not None and pin['trackedLink'] != '' and pin['trackedLink'] != pin['link']):
      res = {}
      res['pinId'] = pin['id']
      res['url'] = pin['trackedLink']
      res['origin'] = 'trackedLink'
      result_list.append(res)

    if (pin['description'] is not None and pin['description'] != ''):
      urls = re.findall(pattern, pin['description'])

      if (urls is not None and len(urls) != 0):
        for url in urls:
          res = {}
          res['pinId'] = pin['id']
          res['url'] = url
          res['origin'] = 'description'
          result_list.append(res)
      
    if (pin['closeupUserNote'] is not None and pin['closeupUserNote'] != ''):
      urls = re.findall(pattern, pin['closeupUserNote'])

      if (urls is not None and len(urls) != 0):
        for url in urls:
          res = {}
          res['pinId'] = pin['id']
          res['url'] = url
          res['origin'] = 'closeupUserNote'
          result_list.append(res)
      
    if (pin['closeupDescription'] is not None and pin['closeupDescription'] != ''):
      urls = re.findall(pattern, pin['closeupDescription'])

      if (urls is not None and len(urls) != 0):
        for url in urls:
          res = {}
          res['pinId'] = pin['id']
          res['url'] = url
          res['origin'] = 'closeupDescription'
          result_list.append(res)
      
  return result_list


if __name__ == '__main__':
  db = dataset.connect('sqlite:///pinterest.db')

  pins = db['pin'].all()

  pins_chunks = grouper(10000, pins)
  pins_chunks_list = []

  for pc in pins_chunks:
    pins_chunks_list.append(pc)

  pool = mp.Pool(processes=50)

  res = pool.map(compile_urls, pins_chunks_list)

  for r in res:
    if (r is not None and (len(r) != 0)):
      db['url'].insert_many(r)
