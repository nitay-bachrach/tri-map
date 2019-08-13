import shelve
import time
import json

import googlemaps
import googlemaps.exceptions
import conf

from exc import *

class Locator(object):
    def __init__(self, cache=conf.CACHE_FILE):
        self._cache = shelve.open(cache)
        self._api = googlemaps.Client(key=conf.KEY)

    def get_location(self, query):
        try:
            cache_key = str(query)
        except UnicodeEncodeError:
            cache_key = repr(query)
        if cache_key in self._cache.keys():
            print 'cached', query
            return self._cache[cache_key]
        time.sleep(1)
        try:
            response = self._api.places(query)
            location = [r['geometry']['location'] for r in response['results']]
            self._cache[cache_key] = location
            return location
        except googlemaps.exceptions.ApiError as e:
            raise MapperException(e.message)
        except googlemaps.exceptions.Timeout:
            raise MapperException("Location timed out")
