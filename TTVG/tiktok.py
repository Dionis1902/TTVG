import time
import requests
import re
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def download_video(url):
    response = requests.post('https://ssstik.io/abc?url=dl', headers=headers,
                             data='gc=0&id=' + urllib.parse.quote(url) + '&locale=en&ss=abc&ts=0&tt=0')

    d = re.findall(r'<a.*href="([^"]*)".*>Without watermark HD</a>', response.text)
    if not d:
        time.sleep(1)
        return download_video(url)

    r = requests.get(d[0], stream=True)

    with open('test.mp4', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    download_video('https://www.tiktok.com/@1niphu/video/7040526638387301637?is_copy_url=1&is_from_webapp=v1&q=%23minecraft%20%23parkour&t=1657049071342')