#!/usr/bin/python

import pysrt
import urllib
import urllib2
from bs4 import BeautifulSoup
import dataset
import multiprocessing as mp
import traceback
import string

URL = 'http://downsub.com/'

def get_url(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')

  resp = urllib2.urlopen(req)
  content = resp.read()

  return content


def get_srts(video_id):
  result_list = []

  try:

    part_url = urllib.urlencode({'url': 'https://www.youtube.com/watch?v=' + video_id})
    url = URL + '?' + part_url

    content = get_url(url)

    dom = BeautifulSoup(content, 'lxml')

    eng_url = dom.find('div', {'id': 'show'}).find_all('b')[0].find_all('a')[0]['href'][2:]

    if not dom.find('div', {'id': 'show'}).contents[2].strip().startswith('English'):
      raise Exception('Correct language not found for video ' + video_id)

    url = URL + eng_url

    content = get_url(url)

    content = filter(lambda x: x in set(string.printable), content)

    subs = pysrt.from_string(content)

    num = 0
    for s in subs:
      result = {'videoId': video_id,
                'startMinutes': s.start.minutes,
                'endMinutes': s.end.minutes,
                'startSeconds': s.start.seconds,
                'endSeconds': s.end.seconds,
                'text': s.text_without_tags,
                'num' : num}

      if (result['endMinutes'] < result['startMinutes']):
        result['endMinutes'] = result['startMinutes']
        result['endSeconds'] = result['startSeconds']

      result_list.append(result)
      num = num + 1

  except:
    print 'Unable to capture subtitles for video %s' % video_id
    traceback.print_exc()
    result_list = []


  return {'result_list': result_list}
 

if __name__ == '__main__':
  db = dataset.connect('sqlite:///youtube.db')

  channels = db.query('SELECT id FROM affiliateVideo')

  channels_list = []
  for row in channels:
    channels_list.append(row['id'])

  pool = mp.Pool(processes=50)

  res = pool.imap_unordered(get_srts, channels_list)

  for r in res:
    if (r is not None and (len(r) != 0)):

      db['captions'].insert_many(r['result_list'])
