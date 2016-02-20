#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Main method
def search_youtube(query):
	set_developer_key()
	return help_search_youtube(query)

# Replace spaces with '\ '
def formatQuery(myQuery):
	myQuery.replace(" ", "\ ")
	return myQuery

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
	formattedQuery = formatQuery(query)

	# Call the search method to retrieve results matching the specified query term
	search_response = youtube.search().list	(
		q=formattedQuery,
		part="id,snippet",
		maxResults=10,
		type="video"
	).execute()

	# List of dictionaries
	videos = []
	
	#Add matching songs to video list
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":

			# Get the url and the video title
			title = search_result["snippet"]["title"]
			url = "%s%s" %("https://www.youtube.com/watch?v=", search_result["id"]["videoId"])

			print "URL: %s Title: %s" %(url, title) 

			# Add to dictionary here
			videos.append({"title":title, "url":url})

	return videos

def main():
	try:
		search_youtube("Community Theme Song")
	except HttpError, e:
		print "An HttpError %d occured: \n %s" % (e.resp.status, e.content)


if __name__ == '__main__':
	main()