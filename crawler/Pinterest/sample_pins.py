#!/usr/bin/python

import requests
import json
import dataset
import time
import multiprocessing as mp
import sys
import logging
import traceback
import crawl_headers as ch
import random
import itertools
from collections import Counter
import pandas as pd
from itertools import izip_longest


def grouper(n, iterable, fillvalue = None):
  args = [iter(iterable)] * n
  return izip_longest(fillvalue = fillvalue, *args)


def details(pin_id):
  print pin_id
  url = 'https://www.pinterest.com/resource/PinResource/get/'
  board_data = {}
  promoter_data = {}
  user_data = []
  pin_data = {}
  
  s = requests.Session()
  for h in ch.pinterest_headers:
    s.headers.update(h)

  try:
    data = '{"options":{"id":"%s","field_set_key":"detailed","is_landing_page":false},"context":{}}' % pin_id

    r = s.get(url, params = {'source_url': '/pin/' + pin_id + '/', 'data': data, '_': time.time()*100}, timeout=10)

    if (r.text is not None):

      jrtext = json.loads(r.text)

      if ('resource_response' in jrtext.keys() and \
          jrtext['resource_response'] != '' and \
          jrtext['resource_response'] is not None and \
          'data' in jrtext['resource_response'].keys() and \
          jrtext['resource_response']['data'] != '' and \
          jrtext['resource_response']['data'] is not None):

        d = jrtext['resource_response']['data']

        pin_data = { 'id': d['id'],
                     'type': d['type'], 
                     'link' : d['link'],
                     'trackedLink': d['tracked_link'],
                     'likeCount': d['like_count'],
                     'isPromoted': d['is_promoted'],
                     'commentCount': d['comment_count'],
                     'method': d['method'],
                     'isRepin': d['is_repin'],
                     'repinCount': d['repin_count'],
                     'priceValue': d['price_value'],
                     'priceCurrency': d['price_currency'],
                     'title' : d['title'],
                     'description': d['description'],
                     'descriptionHTML': d['description_html'],
                     'closeupDescription': d['closeup_description'],
                     'closeupUserNote': d['closeup_user_note'],
                     'createdAt': d['created_at'],
                     'category': d['category'],
                     'ownerId': d['pinner']['id'],
                     'boardId': d['board']['id'] }

         
        if 'rich_metadata' in d.keys() and d['rich_metadata'] != '' and d['rich_metadata'] is not None:
          pin_data['richMetadataSiteName'] = d['rich_metadata']['site_name']
          pin_data['richMetadataDescription'] = d['rich_metadata']['description']
          pin_data['richMetadataTitle'] = d['rich_metadata']['title']
          pin_data['richMetadataLocale'] = d['rich_metadata']['locale']
          pin_data['richMetadataUrl'] = d['rich_metadata']['url']
          pin_data['richMetadataType'] = d['rich_metadata']['type']
          pin_data['richMetadataId'] = d['rich_metadata']['id']

        else:
          pin_data['richMetadataSiteName'] = ''
          pin_data['richMetadataDescription'] = ''
          pin_data['richMetadataTitle'] = ''
          pin_data['richMetadataLocale'] = ''
          pin_data['richMetadataUrl'] = ''
          pin_data['richMetadataType'] = ''
          pin_data['richMetadataId'] = ''



        user = { 'id': d['pinner']['id'],
                 'userName': d['pinner']['username'],
                 'fullName': d['pinner']['full_name'],
                 'type': d['pinner']['type'],
                 'domainUrl': d['pinner']['domain_url'],
                 'domainVerified': d['pinner']['domain_verified'],
                 'location': d['pinner']['location'] }

        user_data.append(user)

        if 'origin_pinner' in d.keys() and d['origin_pinner'] != '' and d['origin_pinner'] is not None:
          user = { 'id': d['origin_pinner']['id'],
                   'userName': d['origin_pinner']['username'],
                   'fullName': d['origin_pinner']['full_name'],
                   'type': d['origin_pinner']['type'],
                   'domainUrl': d['origin_pinner']['domain_url'],
                   'domainVerified': d['origin_pinner']['domain_verified'],
                   'location': d['origin_pinner']['location'] }
          
          user_data.append(user)
          pin_data['originOwnerId'] = user['id']

        else:
          pin_data['originOwnerId'] = ''

        if 'board' in d.keys() and d['board'] != '' and d['board'] is not None:
          board_data = { 'id' : d['board']['id'],
                         'boardOwnerId' : d['board']['owner']['id'],
                         'type' : d['board']['type'],
                         'privacy' : d['board']['privacy'],
                         'url' : d['board']['url'],
                         'name' : d['board']['name'],
                         'description' : d['board']['description'],
                         'category' : d['board']['category'] }

        if 'promoter' in d.keys() and d['promoter'] != '' and d['promoter'] is not None:
          promoter_data = { 'id' : d['promoter']['id'],
                            'userName' : d['promoter']['username'],
                            'fullName' : d['promoter']['full_name'],
                            'type' : d['promoter']['type'] }

          pin_data['promoterId'] = promoter_data['id']

        else:
          pin_data['promoterId'] = ''

      else:
        raise Exception('The required keys were not found in the JSON response for pin %s' % pin_id) 

    else:
      raise Exception('The response was empty')

  except Exception as e:
    print('Caught exception in pin (x = %s):' % pin_id)
    traceback.print_exc()

  return {'pin': pin_data, 'board': board_data, 'promoter': promoter_data, 'user': user_data }


def related_pins_details(pin_id):
  url = 'https://www.pinterest.com/resource/RelatedPinFeedResource/get/'
  pin_data = {}
  
  s = requests.Session()
  for h in ch.pinterest_headers:
    s.headers.update(h)

  pin_list = []
  

  bookmark = None
  offset = 0
  i = 0

  while(True):
    try:

      if bookmark is None:
        data = '{"options":{"pin":"%s","page_size":25,"pins_only":true,"bookmarks":[],"offset":0,"field_set_key":"unauth_react"},"context":{}}' % pin_id
      elif '-end-' in bookmark:
        break
      else:
        data = '{"options":{"pin":"%s","page_size":25,"pins_only":true,"bookmarks":["%s"],"offset":%s,"field_set_key":"unauth_react"},"context":{}}' % (pin_id, bookmark, offset)
        
      r = s.get(url, params = {'source_url': '/pin' + pin_id + '/', 'data': data, 'module_path': 'App(module=[object Object], view_type=content_only)', '_': time.time()*100}, timeout=10)

      if (r.text is not None):

        jrtext = json.loads(r.text)

        if ('resource_response' in jrtext.keys() and \
            jrtext['resource_response'] != '' and \
            jrtext['resource_response'] is not None and \
            'data' in jrtext['resource_response'].keys() and \
            jrtext['resource_response']['data'] != '' and \
            jrtext['resource_response']['data'] is not None):


          for pin in jrtext['resource_response']['data']:
            pin_list.append({'id': pin['id'], 'createdAt': pin['created_at']})

          offset = offset + len(jrtext['resource_response']['data'])

          if (i == 0):
            offset = offset + 3

          i = 1

          bookmark = jrtext['resource']['options']['bookmarks'][0]

          if (offset >= 600):
            break
 
        else:
          raise Exception('The required keys were not found in the JSON response for pin %s' % pin_id) 

      else:
        raise Exception('The response was empty' % pin_id)

    except Exception as e:
      print('Caught exception in pin (x = %s):' % pin_id)
      traceback.print_exc()
      break

  return pin_list


def compile_seeds(seed):
  pin_list = []
  board_list = []
  promoter_list = []
  user_list = []

  pin_seed = seed[:-5]

  for trail in range(1, 1500):

    trail_pad = format(trail, '05')
    pin_id = pin_seed + str(trail_pad)

    r = details(pin_id)

    for user in r['user']:
      if 'id' in user.keys():
        user_list.append(user)

    if 'id' in r['board'].keys():
      board_list.append(r['board'])

    if 'id' in r['promoter'].keys():
      promoter_list.append(r['promoter'])

    if 'id' in r['pin'].keys():
      pin_list.append(r['pin'])

  return {'pin_list': pin_list, 'board_list': board_list, 'promoter_list': promoter_list, 'user_list': user_list}



'''Crawl a set of seed pins across the different categories in Pinterest'''
def crawl_seeds(category):
  url = 'https://www.pinterest.com/resource/CategoryFeedResource/get/'
  results = set()

  s = requests.Session()
  for h in ch.pinterest_headers:
    s.headers.update(h)

  try:
    data ='{"options":{"feed":"%s","is_category":true,"low_price":null,"high_price":null},"context":{},"module":{}}' % category

    r = s.get(url, params = {'source_url': '/categories/' + category + '/', 'data': data, '_': time.time()*100}, timeout=10)

    if (r.text is not None):

      jrtext = json.loads(r.text)

      for d in jrtext['resource_response']['data']:
        results.add(d['id'])

    else:
      raise('The response was empty')

  except Exception as e:
    print e
    raise e

  return list(results)


if __name__ == '__main__':
  db = dataset.connect('sqlite:///pinterest.db')
  cat = db['category'].find(type='main')

  cat_list = [d['key'] for d in cat]

  seeds = []

  for cat in cat_list:
    r = crawl_seeds(cat)
    seeds.extend(r)

  pool = mp.Pool(processes=70)

  res = pool.map(related_pins_details, seeds)

  for r in res:
    if (r is not None and (len(r) != 0)):

      db['pin_seed'].insert_many(r)

  res = db['pin_seed'].all()

  res_list_1 = []
  res_list_2= []
  
  for pin in res:
    res_list_1.append(pin['id'])
    res_list_2.append(pin['createdAt'])

  # Use the sample seeds to being the crawl 
  pool = mp.Pool(processes=70)

  res = pool.map(compile_seeds, df_sample['id'].tolist())

  for r in res:
    if (r is not None and (len(r) != 0)):

      db['user'].insert_many(r['user_list'])

      db['board'].insert_many(r['board_list'])

      db['promoter'].insert_many(r['promoter_list'])

      db['pin'].insert_many(r['pin_list'])
