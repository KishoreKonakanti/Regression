# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 22:49:45 2018

@author: kkonakan
"""

__author__ = 'kkonakan.ai@gmail.com'

import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyDVHPb3k4wf4xpckIv6OjVQ_zoeH0H0YiI")

  res = service.cse().list(
      q='deeplearning',
      cx='017576662512468239146:omuauf_lfve',
    ).execute()
  pprint.pprint(res)

if __name__ == '__main__':
  main()