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


def compile_urls(vids_list):
  result_list = []
  pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

  for vid in vids_list:
    if (vid is None):
      continue

    if (vid['description'] is not None and vid['description'] != ''):
      urls = re.findall(pattern, vid['description'])

      if (urls is not None and len(urls) != 0):
        for url in urls:
          res = {}
          res['videoId'] = vid['id']
          res['url'] = url
          result_list.append(res)
      
  return result_list


if __name__ == '__main__':
  db = dataset.connect('sqlite:///youtube.db')

  vids = db['video'].all()

  vids_chunks = grouper(10000, vids)
  vids_chunks_list = []

  for vc in vids_chunks:
    vids_chunks_list.append(vc)

  pool = mp.Pool(processes=50)

  res = pool.map(compile_urls, vids_chunks_list)

  for r in res:
    if (r is not None and (len(r) != 0)):
      db['url'].insert_many(r)
