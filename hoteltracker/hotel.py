# -*- coding: utf-8 -*-

class HotelWebsite:
    def __init__(self, *args, **kwargs):
        if not all(field in kwargs for field in ('pages', )):
            raise ValueError('Missing required arguments')

    def is_available(self, *args, **kwargs):
        if not all(field in kwargs for field in ('arrival', 'departure')):
            raise ValueError('Missing required arguments')

class Page:
    def __init__(self, *args, **kwargs):
        pass

