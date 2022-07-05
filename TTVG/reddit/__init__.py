import requests
from typing import TypedDict
from TTVG.reddit.exception import *

headers = {
    'User-Agent': 'TTVG'
}


class Post(TypedDict):
    permalink: str
    body: str


class Reddit:
    def __init__(self, client_id, secret):
        self.__auth = (client_id, secret)
        self.__token = None

    def login(self, username, password):
        data = {'grant_type': 'password',
                'username': username,
                'password': password}

        r = requests.post('https://www.reddit.com/api/v1/access_token',
                          auth=self.__auth, data=data, headers=headers)
        if not r.json().get('access_token'):
            raise BadLogin
        self.__token = r.json().get('access_token')

    def __get(self, url, params=None):
        return requests.get(url, params=params, headers={**headers, 'Authorization': f'bearer {self.__token}'})

    def get_posts(self):
        r = self.__get('https://oauth.reddit.com/r/AskReddit/hot', params={'limit': 10, 't': 'day'})
        print(r.text)

    def get_comments(self, url):
        r = self.__get('https://oauth.reddit.com' + url, params={'limit': 10})
        comments = []

        for comment in r.json()[1].get('data', {}).get('children', []):
            if not comment['data'].get('body'):
                continue
            comments.append(Post(permalink=comment['data']['permalink'], body=comment['data']['body']))

        return comments
