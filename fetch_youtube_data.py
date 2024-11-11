import json
from googleapiclient.discovery import build
import os
import logging
from dotenv import load_dotenv
import re

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()  # Load environment variables from .env file

# Client credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube playlist details
PLAYLIST_ID = "PL5ErBr2d3QJH0kbwTQ7HSuzvBb4zIWzhy"

def fetch_youtube_playlist_data(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="snippet,contentDetails", playlistId=playlist_id, maxResults=10, pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()
        
        for item in playlist_response["items"]:
            video_id = item["contentDetails"]["videoId"]
            
            # Fetch additional video details including duration, likes, views, and comments
            video_request = youtube.videos().list(
                part="contentDetails,statistics",
                id=video_id
            )
            video_response = video_request.execute()
            video_details = video_response["items"][0]
            duration = convert_duration(video_details["contentDetails"]["duration"])
            likes = int(video_details["statistics"].get("likeCount", 0))
            views = int(video_details["statistics"].get("viewCount", 0))
            comments = int(video_details["statistics"].get("commentCount", 0))

            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            publishedAt = item["snippet"]["publishedAt"]
            position = item["snippet"].get("position", None)
            thumbnails = item["snippet"]["thumbnails"]
            videoOwnerChannelTitle = item["snippet"].get("videoOwnerChannelTitle", "")
            videoOwnerChannelId = item["snippet"].get("videoOwnerChannelId", "")
            video_link = f"https://www.youtube.com/watch?v={video_id}"

            videos.append({
                "identifier": video_id,
                "blueprint": "youtube_video",
                "title": title,
                "properties": {
                    "title": title,
                    "duration": duration,
                    "link": video_link,
                    "description": description,
                    "publishedAt": publishedAt,
                    "position": position,
                    "likes": likes,
                    "views": views,
                    "comments": comments,
                    "thumbnails": {
                        "default": thumbnails["default"]["url"],
                        "medium": thumbnails["medium"]["url"],
                        "high": thumbnails["high"]["url"],
                        "standard": thumbnails.get("standard", {}).get("url")
                    },
                    "videoOwnerChannelTitle": videoOwnerChannelTitle,
                    "videoOwnerChannelId": videoOwnerChannelId
                },
                "relations": {
                    "playlist": playlist_id
                }
            })

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def fetch_youtube_playlist_info(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        id=playlist_id
    )
    response = request.execute()
    item = response["items"][0]
    
    title = item["snippet"].get("title", "No Title")
    description = item["snippet"].get("description", "").strip() or "No description available"
    published_at = item["snippet"].get("publishedAt", "")
    channel_id = item["snippet"].get("channelId", "")
    channel_title = item["snippet"].get("channelTitle", "")
    thumbnails = item["snippet"].get("thumbnails", {})
    playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"
    
    localized_title = item["snippet"]["localized"].get("title", "No Localized Title")
    localized_description = item["snippet"]["localized"].get("description", "No Localized Description")

    return {
        "identifier": playlist_id,
        "blueprint": "youtube_playlist",
        "title": title,
        "properties": {
            "title": title,
            "link": playlist_link,
            "description": description,
            "publishedAt": published_at,
            "channelId": channel_id,
            "channelTitle": channel_title,
            "thumbnails": {
                "default": thumbnails.get("default", {}).get("url", ""),
                "medium": thumbnails.get("medium", {}).get("url", ""),
                "high": thumbnails.get("high", {}).get("url", ""),
                "standard": thumbnails.get("standard", {}).get("url", "")
            },
            "localized": {
                "title": localized_title,
                "description": localized_description
            }
        }
    }

def convert_duration(duration):
    match = re.match(r'PT((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?', duration)
    if not match:
        return "0:00"

    hours = int(match.group('hours')) if match.group('hours') else 0
    minutes = int(match.group('minutes')) if match.group('minutes') else 0
    seconds = int(match.group('seconds')) if match.group('seconds') else 0

    # Format the duration as "H:MM:SS" or "MM:SS" if no hours are present
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"


def main():
    playlist_data = fetch_youtube_playlist_info(YOUTUBE_API_KEY, PLAYLIST_ID)
    videos_data = fetch_youtube_playlist_data(YOUTUBE_API_KEY, PLAYLIST_ID)
    
    # Combine Playlist and Video data for BULK_UPSERT
    all_data = [playlist_data] + videos_data
    with open("port_entities.json", "w") as f:
        json.dump(all_data, f, indent=4)
    logging.info("Fetched YouTube data and saved to port_entities.json")

if __name__ == "__main__":
    main()
