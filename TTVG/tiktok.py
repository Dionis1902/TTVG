import os
import time
import requests
import re
import urllib.parse


def download_video(url, thread_id):
    url = 'https://www.dropbox.com/s/y45panirur1qm7h/Snaptik_7080454306394148122_zxchneedaim_Full_HD.mp4?dl=1'

    r = requests.get(url, stream=True)

    with open(os.path.join(thread_id, 'bg.mp4'), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
