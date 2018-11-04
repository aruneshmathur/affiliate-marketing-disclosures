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

def channels_list_by_id(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.channels().list(
    **kwargs
  ).execute()

  return response


def grouper(n, iterable, fillvalue = None):
  args = [iter(iterable)] * n
  return izip_longest(fillvalue = fillvalue, *args)


def fill_channel(channel_id_list):
  result_list = []
  update_list = []

  for channel in channel_id_list:

    try:
      if channel is None:
        continue

      result_channel = {'id': channel['channelId']}

      results = channels_list_by_id(service, part='snippet,statistics', id=channel['channelId'])

      if (results is not None and len(results['items']) != 0):
         result_channel['description'] = results['items'][0]['snippet']['description']
         result_channel['title'] = results['items'][0]['snippet']['title']
         result_channel['publishedAt'] = results['items'][0]['snippet']['publishedAt']


         if 'country' in (results['items'][0]['snippet']).keys():
           result_channel['country'] = results['items'][0]['snippet']['country']
         else: 
           result_channel['country'] = ''

         if 'viewCount' in (results['items'][0]['statistics']).keys():
           result_channel['viewCount'] = results['items'][0]['statistics']['viewCount']
         else:
           result_channel['viewCount'] = 0

         if 'commentCount' in (results['items'][0]['statistics']).keys():
           result_channel['commentCount'] = results['items'][0]['statistics']['commentCount']
         else:
           result_channel['commentCount'] = 0

         if 'subscriberCount' in (results['items'][0]['statistics']).keys():
           result_channel['subscriberCount'] = results['items'][0]['statistics']['subscriberCount']
         else:
           result_channel['subscriberCount'] = 0

         if 'videoCount' in (results['items'][0]['statistics']).keys():
           result_channel['videoCount'] = results['items'][0]['statistics']['videoCount']
         else:
           result_channel['videoCount'] = 0

         print result_channel['id']

         result_list.append(result_channel)
         update_list.append({'channelId': result_channel['id'], 'completedStatus': 2})

    except:
      print('Caught exception trying to sample %s:' % result_channel['id'])
      traceback.print_exc() 
      update_list.append({'channelId': result_channel['id'], 'completedStatus': 1})


  return {'result_list': result_list, 'update_list': update_list}


if __name__ == '__main__':
  db = dataset.connect('sqlite:///youtube.db')

  channels = db.query('SELECT (channelId) FROM channelSamples WHERE channelId NOT IN (SELECT channelId FROM channelStatus WHERE completedStatus = 2)')

  channels_chunks = grouper(10000, channels)
  channels_chunks_list = []

  for chan in channels_chunks:
    channels_chunks_list.append(chan)

  pool = mp.Pool(processes=50)

  res = pool.imap_unordered(fill_channel, channels_chunks_list)

  for r in res:
    if (r is not None and (len(r) != 0)):

      db['channel'].insert_many(r['result_list'])

      db['channelStatus'].insert_many(r['update_list'])
