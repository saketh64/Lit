#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from youtube_filter import filter_results

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Main method
def search_youtube(query,enable_filter=True):
    set_developer_key()
    result = help_search_youtube(query)
    if enable_filter:
        return filter_results(result)
    else:
        return result


# Replace spaces with '\ '
def format_query(my_query):
    my_query.replace(" ", "\ ")
    return my_query


# Sets the developer key
def set_developer_key():
    f = open("key.txt")
    line = f.readline()
    global DEVELOPER_KEY
    DEVELOPER_KEY = line


# Helper method that returns a list of dictionaries for video titles and urls
def help_search_youtube(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Parse the query
    formatted_query = format_query(query)

    # Call the search method to retrieve results matching the specified query term
    search_response = youtube.search().list(
        q=formatted_query,
        part="id,snippet",
        maxResults=30,
        type="video"
    ).execute()

    # List of dictionaries
    videos = []

    # Add matching songs to video list
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # Get the url and the video title
            title = search_result["snippet"]["title"]
            url = "%s%s" % ("https://www.youtube.com/watch?v=", search_result["id"]["videoId"])

            # Add to dictionary here
            videos.append(YouTubeSearchResult(title,url))

    return videos

class YouTubeSearchResult():
    """
    fields (all are strings or None):
        youtube_title
        url
        artist
        title
    """
    def __init__(self,youtube_title,url):
        self.youtube_title = youtube_title
        self.url = url

        # We'll attempt to parse these from the video title
        self.artist = None
        self.title = None

    def __eq__(self,other):
        """Checks title/artist equality if possible, otherwise just uses url"""
        if not isinstance(other,YouTubeSearchResult):
            return False

        if self.artist is not None and other.artist is not None:
            return self.artist == other.artist and self.song_title == other.song_title
        else:
            return self.url == other.url
