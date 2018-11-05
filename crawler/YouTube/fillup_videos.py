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


def videos_list_by_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)
  results = service.videos().list(
    **kwargs
  ).execute()
  
  return results


def grouper(n, iterable, fillvalue = None):
  args = [iter(iterable)] * n
  return izip_longest(fillvalue = fillvalue, *args)


def fill_videos(video_id_list):
  result_list = []
  update_list = []

  for video in video_id_list:

    try:
      if video is None:
        continue

      time.sleep(0.5)

      result_video = {'id': video['id']}

      results = videos_list_by_id(service, part='snippet,contentDetails,statistics', id=video['id'])

      if (results is not None and len(results['items']) != 0):
         result_video['description'] = results['items'][0]['snippet']['description']
         result_video['categoryId'] = results['items'][0]['snippet']['categoryId']
         result_video['title'] = results['items'][0]['snippet']['title']
         result_video['channelId'] = results['items'][0]['snippet']['channelId']
         result_video['publishedAt'] = results['items'][0]['snippet']['publishedAt']


         if 'viewCount' in (results['items'][0]['statistics']).keys():
           result_video['viewCount'] = results['items'][0]['statistics']['viewCount']
         else: 
           result_video['viewCount'] = 0

         if 'likeCount' in (results['items'][0]['statistics']).keys():
           result_video['likeCount'] = results['items'][0]['statistics']['likeCount']
         else:
           result_video['likeCount'] = 0

         if 'dislikeCount' in (results['items'][0]['statistics']).keys():
           result_video['dislikeCount'] = results['items'][0]['statistics']['dislikeCount']
         else:
           result_video['dislikeCount'] = 0

         if 'favoriteCount' in (results['items'][0]['statistics']).keys():
           result_video['favoriteCount'] = results['items'][0]['statistics']['favoriteCount']
         else:
           result_video['favoriteCount'] = 0

         if 'commentCount' in (results['items'][0]['statistics']).keys():
           result_video['commentCount'] = results['items'][0]['statistics']['commentCount']
         else:
           result_video['commentCount'] = 0

         if 'defaultAudioLanguage' in (results['items'][0]['snippet']).keys():
           result_video['defaultLanguage'] = results['items'][0]['snippet']['defaultAudioLanguage']
         else:
           result_video['defaultLanguage'] = ''

         result_video['duration'] = results['items'][0]['contentDetails']['duration']

         result_list.append(result_video)
         update_list.append({'sampleVideoId': video['id'], 'completedStatus': 2})

    except:
      print('Caught exception trying to sample %s:' % video['id'])
      traceback.print_exc() 
      update_list.append({'sampleVideoId': video['id'], 'completedStatus': 1})


  return {'result_list': result_list, 'update_list': update_list}


if __name__ == '__main__':
  db = dataset.connect('sqlite:///youtube.db')

  videos = db.query('SELECT * FROM sampleVideos WHERE id NOT IN (SELECT sampleVideoId FROM sampleVideosStatus WHERE completedStatus = 2)')

  videos_chunks = grouper(1000, videos)
  videos_chunks_list = []

  for vid in videos_chunks:
    videos_chunks_list.append(vid)

  pool = mp.Pool(processes=50)

  res = pool.imap_unordered(fill_videos, videos_chunks_list)

  for r in res:
    if (r is not None and (len(r) != 0)):
      db['video'].insert_many(r['result_list'])

      db['sampleVideosStatus'].insert_many(r['update_list'])
