import youtube_dl
import sys
import subprocess

TYELLOW = '\033[33m'
TWHITE = '\033[37m'


class Player:
    def __init__(self):
        print("Pause - p, Mute audio - m")


    def play_song(self, url):
        youtube_dl_obj = youtube_dl.YoutubeDL({'quiet': True})
        song_title = youtube_dl_obj.extract_info(url, False)['title']
        print(TYELLOW + f'  ♫ %s ' % song_title + TWHITE, end='\r')
        cmd = 'mpv {} --really-quiet -no-video --audio-display=no'.format(url)
        subprocess.Popen(cmd.split()).wait()
        print(f"\r    %s" % song_title)
