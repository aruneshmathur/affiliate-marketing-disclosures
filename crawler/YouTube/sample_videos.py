#!/usr/bin/python

import string
import requests
import json
import time
import dataset
import numpy as np
from itertools import izip_longest
import multiprocessing as mp
import logging
import traceback
from ytlibrary import *

def search_list_by_keyword(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) 
  results = service.search().list(**kwargs).execute()
 
  return results


def init_samples():
  chars = []
  chars.extend(range(0,10))
  chars.extend(['_', '-'])
  chars.extend(list(string.ascii_lowercase))

  sample_list = []
  for i in range(0, 1000000):
    sample_list.append({ 'seed': ''.join([str(x) for x in np.random.choice(chars, 5)]),
                         'resultsCount': 0,
                         'completedStatus': 0})

  return sample_list


def grouper(n, iterable, fillvalue = None):
  args = [iter(iterable)] * n
  return izip_longest(fillvalue = fillvalue, *args)


def fill_samples(sample_list):
  result_sample_list = []
  result_sample_video_list = []

  for sample in sample_list:
    try:
      if sample is None:
        continue

      watch = '"watch?v=%s"' % sample['seed']
      result_sample = {'autoId': sample['autoId']}

      jrtext = search_list_by_keyword(service, part='snippet', maxResults=50, q=watch, type='video')
      time.sleep(1)
 
      if jrtext is not None:

        if 'pageInfo' in jrtext.keys():

          count = jrtext['pageInfo']['totalResults']
          result_sample['resultsCount'] = count
          print 'Count' + str(count)

          if count <= 50:
            result_sample['completedStatus'] = 2

            for item in jrtext['items']:
              result_sample_video_list.append({'id': item['id']['videoId'], 'sampleId': sample['autoId']})
          
          else:
            result_sample['completedStatus'] = 1

          result_sample_list.append(result_sample)

    except:
      print('Caught exception trying to sample %s:' % sample['seed'])
      traceback.print_exc() 


  return {'result_sample_list': result_sample_list, 'result_sample_video_list': result_sample_video_list}


if __name__ == '__main__':
  db = dataset.connect('sqlite:///youtube.db')

  result = init_samples()
  db['sample'].insert_many(result)

  samples = db['sample'].find(completedStatus = 0, _limit = 9000)

  sample_chunks = grouper(10000, samples)
  sample_chunks_list = []

  for sc in sample_chunks:
    sample_chunks_list.append(sc)

  pool = mp.Pool(processes=3)

  res = pool.map(fill_samples, sample_chunks_list)

  for r in res:
    if (r is not None and (len(r) != 0)):

      db['sampleVideos'].insert_many(r['result_sample_video_list'])

      for sample in r['result_sample_list']:
        db['sample'].update(sample, ['autoId'])
