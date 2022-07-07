import os
from TTVG import VideoMaker

video_maker = VideoMaker(os.environ.get('CLIENT_ID'), os.environ.get('SECRET'),
                         os.environ.get('USERNAME'), os.environ.get('PASSWORD'))


video_maker.make_video()