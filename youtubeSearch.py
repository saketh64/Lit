#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyB_o1C4U6-YjhHvbW8IkWzQxt2ZZFy6FqI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	# Call the search method to retrieve results matching the specified query term
	search_response = youtube.search().list	(
		q=options.q,
		part="id,snippet",
		maxResults=options.max_results
	).execute()

	videos = []
	
	#Add matching songs to video list
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]) )

	print "Videos:\n", "\n".join(videos), "\n"



def main():
	argparser.add_argument("--q", help= "Search Term", default="Google")
	argparser.add_argument("--max-results", help="Max Results", default=25)
	args = argparser.parse_args()

	try:
		youtube_search(args)
	except HttpError, e:
		print "An HttpError %d occured: \n %s" % (e.resp.status, e.content)


if __name__ == '__main__':
	main()