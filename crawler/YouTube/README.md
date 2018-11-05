## Overview

This folder contains scripts to gather a sample of YouTube videos. For more details on the sampling method, please go through Section 3.1.1 of the [paper](https://arxiv.org/pdf/1809.00620.pdf).

## Description of files

* `database_schema.sql`: As the crawler proceeds, it stores the data it collects;  this schema file can be used to set up the SQLite3 database tables
* `fillup_captions.py`: For each video, collects the closed captions (if available) from DownSub
* `fillup_channels.py`: Collects the channels corresponding to the sampled videos
* `fillup_videos.py`: Collects information about the sampled videos
* `retrieve_urls.py`: Extracts URLs from the videos and stores them
* `sample_videos.py`: Sample videos from YouTube
* `youtube.db`: The sample of videos used in this analysis; stored in a SQLite3 database

These files use the [YouTube Data API](https://developers.google.com/youtube/v3/) library underneath. The library needs to be set up before the files can be run. `ytlibrary.py` is YouTube's Python wrapper around their API.
