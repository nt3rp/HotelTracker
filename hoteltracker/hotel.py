# -*- coding: utf-8 -*-
import collections

class HotelWebsite:
    # TODO: Do we really need kwargs? Why not just define the kwargs?
    def __init__(self, *args, **kwargs):
        if not all(field in kwargs for field in ('pages', )):
            raise ValueError('Missing required arguments')

        for key, value in kwargs.iteritems():
            new_key = '_{key}'.format(key=key)
            setattr(self, new_key, value)

        if not isinstance(self._pages, collections.Iterable):
            raise TypeError('\'self.pages\' is not iterable')


    def is_available(self, *args, **kwargs):
        if not all(field in kwargs for field in ('arrival', 'departure')):
            raise ValueError('Missing required arguments')

class Page:
    def __init__(self, *args, **kwargs):
        pass

