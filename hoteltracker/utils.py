# -*- coding: utf-8 -*-
from collections import deque
import json
import logging
import random
import twitter
from datetime import datetime

def list_missing_args(required=(), provided=(), message=None):
    difference = set(required) - set(provided)

    if not message:
        return difference

    return message.format(args=', '.join(difference),
        s='s'[len(difference)==1:])

class TwitterHandler(logging.Handler):
    POST_ATTEMPTS = 3
    START = {
        "positive": [
            "",
            "Hooray! ", "Hooray; ",
            "Success! ", "Success; "
                         "Huzzah! ", "Huzzah; "
                                     "Yay! ", "Yay; "
        ],
        "negative": [
            "",
            "Boo! ", "Boo; ",
            "Dang! ", "Dang; ",
            "Fail! ", "Fail; "
        ]
    }
    END = {
        "positive":  ["", "!", ".", "…", "♪", "✔"],
        "negative":  ["", "!", ".", "…", "✖"]
    }

    def __init__(self, config=None, atoken=None, asecret=None,
                 ctoken=None, csecret=None, **kwargs):
        logging.Handler.__init__(self, **kwargs)

        if kwargs.get('config'):
            with open(kwargs.get('config'), 'r') as f:
                obj    = json.loads(f.read())
                atoken  = obj.get('access_token')
                asecret = obj.get('access_secret')
                ctoken  = obj.get('consumer_token')
                csecret = obj.get('consumer_secret')

        # TODO: Do something if missing tokens

        # Twitter API code
        self._api = twitter.Api(
            consumer_key=ctoken,
            consumer_secret=csecret,
            access_token_key=atoken,
            access_token_secret=asecret)

        if not self._api.VerifyCredentials():
            raise ValueError("Could not connect to Twitter")

    def emit(self, record):
        if getattr(record, 'tweet', False):
            hotel = getattr(record, 'hotel')
            success = getattr(record, 'success')
            now = datetime.now()
            info = self._update_info(hotel, success, now)

            state = self._get_state(info, now)
            if state['changed'] or not info['last_update']:
                self._post_changed(info)
                info['last_update'] = now
            elif state['stale']:
                self._post_stale(info)
                info['last_update'] = now
            else:
                logging.info("update: No need to update")

    # Private functions
    def _get_state(self, info, now=datetime.now()):
        return {
            'stale'  : self.is_stale(info['last_update'], now=now),
            'changed': self.is_changed(*info['last_results'])
        }

    def _update_info(self, hotel, success, now=datetime.now()):
        info = self._hotels.get(hotel, {
            'last_update': None,
            'last_results': deque([], maxlen=2),
            'name': hotel
        })
        info['last_results'].append(success)
        self._hotels[hotel] = info
        return self._hotels[hotel]

    def _post(self, info, message):
        success = list(info['last_results'])[-1]

        if success:
            (num_rooms, tone) = ("at least one room", "positive")
        else:
            (num_rooms, tone) = ("no rooms", "negative")

        unposted = True
        attempts = 0
        while unposted and (attempts < self.POST_ATTEMPTS):
            f_message = message.format(
                hotel=info['name'],
                num_rooms=num_rooms,
                start=random.choice(self.START[tone]),
                end=random.choice(self.END[tone])
            )
            logging.info('_post: {0}'.format(f_message))

            try:
                status = self._api.PostUpdate(f_message)
            except twitter.TwitterError, e:
                logging.error('_post: {0}'.format(e))
                attempts += 1
            else:
                logging.info('_post: {0}'.format(status))
                unposted = False

    def _post_stale(self, info):
        self._post(info, "{hotel}: {start}still {num_rooms} available{end}")

    def _post_changed(self, info):
        self._post(info, "{hotel}: {start}{num_rooms} available{end}")

    # Public functions
    def update(self, hotel, success):
        now   = datetime.now()
        info  = self._update_info(hotel, success, now)

        state = self._get_state(info, now)
        if state['changed'] or not info['last_update']:
            self._post_changed(info)
            info['last_update'] = now
        elif state['stale']:
            self._post_stale(info)
            info['last_update'] = now
        else:
            logging.info("update: No need to update")

    # Static and class methods
    @staticmethod
    def is_changed(prev=False, next=False):
        return prev != next

    @staticmethod
    def is_stale(last_update, now=datetime.now(), stale_duration=14400):
        if not last_update:
            return False
        return (now - last_update).seconds >= stale_duration