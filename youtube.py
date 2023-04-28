import os
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd

# Set DEVELOPER_KEY to the API key value from the APIs & Services > Credentials
# tab of your Google Cloud Console project.
DEVELOPER_KEY = "AIzaSyCJIPXQboD4ExbjP8SlXi6mlbvjPCslqMQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Set the video ID of the YouTube video you want to retrieve comments for.
VIDEO_ID = "Gi1vGwcTftc"

# Set the maximum number of comments to retrieve. You can adjust this as needed.
MAX_RESULTS = 100

# Build the YouTube API client.
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Retrieve the video's comment threads.
threads = []
results = youtube.commentThreads().list(
    part="snippet",
    videoId=VIDEO_ID,
    maxResults=MAX_RESULTS
).execute()
while results:
    threads += results["items"]
    # Check if there are more comments to retrieve.
    if "nextPageToken" in results:
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=VIDEO_ID,
            maxResults=MAX_RESULTS,
            pageToken=results["nextPageToken"]
        ).execute()
    else:
        break

# Parse the comment data and write it to a CSV file.
path = os.path.join(os.path.dirname(__file__), "", "comments.csv")  # Set the desired path here.
with open(path, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["Comment", "Author", "Date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for thread in threads:
        comment = thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        author = thread["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        date = thread["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        writer.writerow({"Comment": comment, "Author": author, "Date": date})

# Load the comments data into a pandas DataFrame.
df = pd.read_csv(path)

# Display the comments data.
print(df.head())
