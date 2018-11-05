## Overview

This folder contains scripts to gather a sample of Pinterest pins. For more details on the sampling method, please go through Section 3.1.1 of the [paper](https://arxiv.org/pdf/1809.00620.pdf).

## Description of files

* `crawl_headers.py`: Contains the headers required for this Pinterest crawler
* `database_schema.sql`: As the crawler proceeds, it stores the data it collects; this schema file can be used to set up the SQLite3 database tables
* `pinterest.db.zip`: The sample of pins used in this analysis; stored in a SQLite3 database
* `retrieve_urls.py`: Extracts URLs from the pins and stores them
* `sample_pins.py`: Sample pins from Pinterest
