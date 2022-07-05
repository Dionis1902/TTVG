from TTVG import Reddit
import os
from TTVG.image import Screenshot


def get_comments(thread_id):
    reddit = Reddit(os.environ.get('CLIENT_ID'), os.environ.get('SECRET'))
    reddit.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))

    comments = reddit.get_comments('/r/AskReddit/comments/' + thread_id)
    image = Screenshot()
    image.save_title(comments[0]['permalink'])
    for i in comments:
        image.save_comment(i['permalink'])


get_comments('vpn1vj')