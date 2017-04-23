=====
About
=====

This is https://www.tevu-darzelis.lt/vaiku-vardai/ scraper.
It scrapes child names in Lithuania statistics.
It requires Python >= 3.6.

Usage
=====

Scrape all name URLS and save output to json formatted file::

    pyenv/bin/scrapy runspider vardai_scraper/spiders.py -o urls.json

Setup
=====

Create python virtual environment::

    $ make pyenv

This command will download and install all project dependencies to `pyenv/`
directory.
