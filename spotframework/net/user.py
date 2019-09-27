import requests
from spotframework.model.user import User
from spotframework.util.console import Color
from base64 import b64encode
import logging
import time
from typing import Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class NetworkUser(User):

    def __init__(self, client_id, client_secret, refresh_token, access_token=None):
        super().__init__('')

        self.accesstoken = access_token
        self.refreshtoken = refresh_token

        self.client_id = client_id
        self.client_secret = client_secret

        self.last_refreshed = None
        self.token_expiry = None

        self.on_refresh = []

    def __repr__(self):
        return Color.RED + Color.BOLD + 'NetworkUser' + Color.END + \
               f': {self.username}, {self.display_name}, {self.uri}'

    def refresh_token(self) -> None:

        if self.refreshtoken is None:
            raise NameError('no refresh token to query')

        if self.client_id is None:
            raise NameError('no client id')

        if self.client_secret is None:
            raise NameError('no client secret')
        
        idsecret = b64encode(bytes(self.client_id + ':' + self.client_secret, "utf-8")).decode("ascii")
        headers = {'Authorization': 'Basic %s' % idsecret}

        data = {"grant_type": "refresh_token", "refresh_token": self.refreshtoken}

        now = datetime.now(timezone.utc)
        req = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
   
        if 200 <= req.status_code < 300:
            logger.debug('token refreshed')
            resp = req.json()
            self.accesstoken = resp['access_token']
            self.token_expiry = resp['expires_in']
            self.last_refreshed = now
            for func in self.on_refresh:
                func(self)
        else:

            if req.status_code == 429:
                retry_after = req.headers.get('Retry-After', None)

                if retry_after:
                    logger.warning(f'refresh_token rate limit reached: retrying in {retry_after} seconds')
                    time.sleep(int(retry_after) + 1)
                    return self.refresh_token()
                else:
                    logger.error('refresh_token rate limit reached: cannot find Retry-After header')

            else:
                error_text = req.json()['error']['message']
                logger.error(f'refresh_token get {req.status_code} {error_text}')

    def refresh_info(self) -> None:
        info = self.get_info()

        if info.get('display_name', None):
            self.display_name = info['display_name']

        if info.get('external_urls', None):
            if info['external_urls'].get('spotify', None):
                self.ext_spotify = info['external_urls']['spotify']

        if info.get('href', None):
            self.href = info['href']

        if info.get('id', None):
            self.username = info['id']

        if info.get('uri', None):
            self.uri = info['uri']

    def get_info(self) -> Optional[dict]:
        
        headers = {'Authorization': 'Bearer %s' % self.accesstoken}

        req = requests.get('https://api.spotify.com/v1/me', headers=headers)

        if 200 <= req.status_code < 300:
            logger.debug(f'retrieved {req.status_code}')
            return req.json()
        else:

            if req.status_code == 429:
                retry_after = req.headers.get('Retry-After', None)

                if retry_after:
                    logger.warning(f'get_info rate limit reached: retrying in {retry_after} seconds')
                    time.sleep(int(retry_after) + 1)
                    return self.get_info()
                else:
                    logger.error('get_info rate limit reached: cannot find Retry-After header')

            elif req.status_code == 401:
                logger.warning('access token expired, refreshing')
                self.refresh_token()
                return self.get_info()

            else:
                error_text = req.json()['error']['message']
                logger.error(f'get_info get {req.status_code} {error_text}')
