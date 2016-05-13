"""
audio_manager.py

This module is used to queue/download audio from Youtube to the Lit server.

It uses pafy for the Youtube audio downloads.

'set_on_download_completed' should be called from main.py to attach an event for when a song is
finished downloading - we will notify certain nowplaying sessions that their song is ready, etc.
"""

import pafy
import os
from threading import Thread

import logging


logger = logging.getLogger("AM")

BASE_URL = "https://www.youtube.com/watch?v=%s"
STORAGE_PATH = "flask_app/static/music/%s.mp3"

class SongState:
    DOWNLOADED = 0
    QUEUED = 1
    NONE = 2

queue = []

def _(url):
    pass

on_download_completed = _

def set_on_download_completed(event_handler):
    global on_download_completed
    on_download_completed = event_handler

def get_id_from_url(url):
    ID_idx = url.index("watch?v=")+8
    return url[ID_idx:]

def download_song(url):
    id = get_id_from_url(url)
    logger.info("Downloading song with ID: %s" % id)
    if get_song_state(url) == SongState.DOWNLOADED:
        logger.info("Skipping download of song with ID: %s" % id)
        return
    video = pafy.new(url)
    stream = video.getbestaudio()
    stream.download(STORAGE_PATH % id)
    logger.info("Finishing download of song with ID: %s" % id)
    on_download_completed(url)

def _queue_song(url):
    """ this is called from a background thread """
    id = get_id_from_url(url)
    logger.info("Queueing song with ID: %s" % id)
    # if queue is empty, download the song
    if len(queue) == 0:
        queue.append(url)
        download_song(url)
        queue.pop(0)
        on_downloader_ready()
    else:
        queue.append(url)

def queue_song(url):
    t = Thread(target=_queue_song,args=(url,))
    t.start()

def on_downloader_ready():
    if len(queue) > 0:
        download_song(queue[0])
        queue.pop(0)
        on_downloader_ready()

def remove_song(url):
    id = get_id_from_url(url)
    path = STORAGE_PATH % id
    if os.path.exists(path):
        os.remove(path)
    else:
        pass

def get_song_state(url):
    id = get_id_from_url(url)
    path = STORAGE_PATH % id
    if os.path.exists(path):
        return SongState.DOWNLOADED
    else:
        return SongState.QUEUED

'''
#########################
#       TESTING         #
#########################
from threading import Thread
from time import sleep
from random import random


def test(url):
    sleep(random()*2)
    queue_song(url)

urls = ["https://www.youtube.com/watch?v=LkWpURhvN3E",
        "https://www.youtube.com/watch?v=J-vUJx8swoU",
        "https://www.youtube.com/watch?v=f7plhrsQSEE",
        "https://www.youtube.com/watch?v=68oooLfnoIw"]


for u in urls:
    t = Thread(target=test,args=(u,))
    t.start()
'''