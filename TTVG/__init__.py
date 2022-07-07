import random
from TTVG.reddit import Reddit
from TTVG.image_generator import Screenshot
from TTVG.text import get_voice_text
import redis
from TTVG.tiktok import download_video
import glob
import math
import shutil
import moviepy.editor as mp
from moviepy.video.compositing.concatenate import concatenate
from moviepy.video.fx.resize import resize
import os
from TTVG.voice import Voice


class VideoMaker:
    def __init__(self, client_id, secret, username, password, host='localhost', port=6379):
        self._rd = redis.Redis(host=host, port=port, db=0)
        self._reddit = Reddit(client_id, secret)
        self._reddit.login(username, password)

    def _get_post_id(self, subreddit):
        posts = self._reddit.get_posts(subreddit)
        for post in posts:
            if self._rd.get('used:' + post):
                continue
            self._rd.set('used:' + post, 1)
            return post

    @staticmethod
    def download_bg(thread_id):
        with open('bg.txt', 'r') as f:
            download_video(random.choice(f.readlines()), thread_id)

    def prepare_all(self, post_id, lang, subreddit):
        comments, title = self._reddit.get_comments(post_id, subreddit)
        if not os.path.exists(post_id):
            os.mkdir(post_id)
        self.download_bg(post_id)
        screenshot = Screenshot()
        v = Voice(token)
        screenshot.save_title(comments[0]['permalink'], os.path.join(post_id, 'title.png'))
        v.generate_voice(get_voice_text(title), os.path.join(post_id, f'title.mp3'))
        for i, comment in enumerate(comments):
            screenshot.save_comment(comment['permalink'], os.path.join(post_id, f'comment_{i}.png'))
            v.generate_voice(get_voice_text(comment['body']), os.path.join(post_id, f'audio_{i}.mp3'))

    @staticmethod
    def prepare_image(image_path, audio_path, width, image_pause=.15, margin=20):
        audio = mp.AudioFileClip(os.path.join(audio_path))
        image = mp.ImageClip(image_path, duration=audio.duration + image_pause).set_audio(audio)
        return resize(image, (width - margin) / image.size[0])

    def make_video(self, lang='en', subreddit='AskReddit'):
        post_id = self._get_post_id(subreddit)
        self.prepare_all(post_id, lang, subreddit)
        bg = mp.VideoFileClip(os.path.join(post_id, 'bg.mp4')).volumex(0.02)
        images = [self.prepare_image(os.path.join(post_id, 'title.png'),
                                     os.path.join(post_id, 'title.mp3'), bg.size[0])]

        for image, audio in zip(sorted(glob.glob(os.path.join(post_id, 'comment_*.png'))),
                                sorted(glob.glob(os.path.join(post_id, 'audio_*.mp3')))):
            images.append(self.prepare_image(image, audio, bg.size[0]))

        images_clip = concatenate(images, method='compose')
        duration = sum(map(lambda x: x.__dict__['duration'], images))
        bg = concatenate([bg] * math.ceil(duration / bg.duration), method='compose')
        final = mp.CompositeVideoClip([bg, images_clip.set_position("center")]).set_duration(duration)
        final.write_videofile(post_id + '.mp4', threads=8, temp_audiofile='temp-audio.m4a', remove_temp=True,
                              codec='libx264', audio_codec='aac')
        shutil.rmtree(post_id)
