import re
import os
from pprint import pprint


class AudioPostProcess:
    def __init__(self, storage_dir):
        pass

    def _download(self):
        os.system(
            '''{} ffmpeg -i $(youtube-dl -f bestaudio -g {}) -ss 0 -to 0:0:1 -ab 192k -af loudnorm=I=-16:TP=-2:LRA=11 -vn {}.opus'''
            .format()
        )


if __name__ == '__main__':
    a = AudioPostProcess("a")
    a._normalize()
