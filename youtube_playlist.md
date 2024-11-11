
# YouTube Playlist & Videos Catalog in Port

This guide will help you set up an automated process to catalog YouTube playlist and video data into Port. Using Port's GitHub action, you’ll fetch YouTube data and ingest it into Port for easy tracking and visualization.

## Prerequisites

1. [Create a Port account](https://app.getport.io) and set up API credentials.
2. [Obtain a YouTube Data API Key](https://console.cloud.google.com/apis/credentials).
3. [Set up GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in your repository for:
   - `YOUTUBE_API_KEY`: Your YouTube API key.
   - `CLIENT_ID`: Your Port client ID.
   - `CLIENT_SECRET`: Your Port client secret.

## Step 1: Model Data in Port


Define two blueprints in Port: `youtube_playlist` for playlists and `youtube_video` for individual videos.

### Playlist Blueprint (`youtube_playlist`)

- **Properties**:
  - `title` (string): Title of the playlist.
  - `link` (string): YouTube URL of the playlist.
  - `description` (string): Description of the playlist.
  - `publishedAt` (string): Publish date of the playlist.
  - `channelId` (string): ID of the YouTube channel that owns the playlist.
  - `channelTitle` (string): Title of the YouTube channel that owns the playlist.
  - `thumbnails` (object): Thumbnail images in various resolutions (default, medium, high, standard).
  - `localized` (object): Localized information with properties for `title` and `description`.
  
---

   <details>
     <summary>Configuration mapping for playlist blueprint (click to expand)</summary>

```json showLineNumbers
{
    "identifier": "youtube_playlist",
    "title": "YouTube Playlist",
    "description": "Blueprint for YouTube Playlist",
    "schema": {
        "properties": {
            "title": { "type": "string", "title": "Playlist Title" },
            "link": { "type": "string", "title": "Playlist Link" },
            "description": { "type": "string", "title": "Playlist Description" },
            "publishedAt": { "type": "string", "title": "Publish Date" },
            "channelId": { "type": "string", "title": "Channel ID" },
            "channelTitle": { "type": "string", "title": "Channel Title" },
            "thumbnails": {
                "type": "object",
                "title": "Thumbnails",
                "properties": {
                    "default": { "type": "string", "title": "Default Thumbnail" },
                    "medium": { "type": "string", "title": "Medium Thumbnail" },
                    "high": { "type": "string", "title": "High Thumbnail" },
                    "standard": { "type": "string", "title": "Standard Thumbnail" }
                }
            },
            "localized": {
                "type": "object",
                "title": "Localized Information",
                "properties": {
                    "title": { "type": "string", "title": "Localized Title" },
                    "description": { "type": "string", "title": "Localized Description" }
                }
            }
        },
        "required": ["title", "description", "publishedAt", "channelId", "channelTitle"]
    },
    "mirrorProperties": {},
    "calculationProperties": {},
    "aggregationProperties": {},
    "relations": {}
}
```
   </details>

---

### Video Blueprint (`youtube_video`)

- **Properties**:
  - `title` (string): Title of the video.
  - `link` (string): YouTube URL of the video.
  - `duration` (string): Duration of the video.
  - `description` (string): Description of the video.
  - `publishedAt` (string): Publish date of the video.
  - `position` (number): Position in the playlist.
  - `likes` (number): Number of likes on the video.
  - `views` (number): Number of views on the video.
  - `comments` (number): Number of comments on the video.
  - `thumbnails` (object): Thumbnail images in various resolutions (default, medium, high, standard, maxres).
  - `videoOwnerChannelTitle` (string): Title of the owner channel.
  - `videoOwnerChannelId` (string): ID of the owner channel.
- **Relationships**:
  - `playlist`: Links to the `youtube_playlist` entity.

---

   <details>
     <summary>Configuration mapping for video blueprint (click to expand)</summary>
     
```json showLineNumbers
{
    "identifier": "youtube_video",
    "title": "YouTube Video",
    "description": "Blueprint for YouTube Video",
    "schema": {
        "properties": {
            "title": { "type": "string", "title": "Video Title" },
            "link": { "type": "string", "title": "Video Link" },
            "duration": { "type": "string", "title": "Video Duration" },
            "description": { "type": "string", "title": "Video Description" },
            "publishedAt": { "type": "string", "title": "Publish Date" },
            "position": { "type": "number", "title": "Position in Playlist" },
            "likes": { "type": "number", "title": "Like Count" },
            "views": { "type": "number", "title": "View Count" },
            "comments": { "type": "number", "title": "Comment Count" },
            "thumbnails": {
                "type": "object",
                "title": "Thumbnails",
                "properties": {
                    "default": { "type": "string", "title": "Default Thumbnail" },
                    "medium": { "type": "string", "title": "Medium Thumbnail" },
                    "high": { "type": "string", "title": "High Thumbnail" },
                    "standard": { "type": "string", "title": "Standard Thumbnail" },
                    "maxres": { "type": "string", "title": "Max Resolution Thumbnail" }
                }
            },
            "videoOwnerChannelTitle": { "type": "string", "title": "Channel Title" },
            "videoOwnerChannelId": { "type": "string", "title": "Channel ID" }
        },
        "required": ["title", "description", "publishedAt", "duration", "link"]
    },
    "mirrorProperties": {},
    "calculationProperties": {},
    "aggregationProperties": {},
    "relations": {
        "playlist": {
            "title": "Playlist",
            "many": false,
            "target": "youtube_playlist",
            "required": true
        }
    }
}


```
   </details>

---

### Create the `youtube_playlist` & `youtube_playlist` Blueprints in Port

1. Navigate to the `Builder` in your Port header section [Builder](https://app.getport.io/settings/data-model).
2. Click over the `+ Blueprint` button, and select `Edit JSON`.
2. On the `New Blueprint` modal popup, click on the `Edit JSON` button on the right.
3. Add the configuration mapping json object for both blueprints :


Here’s an example of what you would see on Port when trying to create blueprints.

--- 

<img src='/img/blueprint.png' border='1px' />

---

<img src='/img/data_model.png' border='1px' />

---

## Step 2: GitHub Workflow for Data Ingestion

The following GitHub workflow automates fetching data from YouTube and updating Port with the data.

### GitHub Workflow (`.github/workflows/youtube_port_workflow.yml`)

```yaml showLineNumbers
name: Update YouTube Playlist and Video Entities in Port

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight

jobs:
  update_port_entities:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run YouTube Data Fetch and Prepare Port Entities
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          CLIENT_ID: ${{ secrets.CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
        run: python fetch_youtube_data.py

      - name: Bulk Create/Update YouTube Playlist and Video Entities in Port
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.CLIENT_ID }}
          clientSecret: ${{ secrets.CLIENT_SECRET }}
          baseUrl: https://api.getport.io
          operation: BULK_UPSERT
          entities: ${{ toJson(fromJson(file('port_entities.json'))) }}
```

---

### Fetch YouTube Data

The `fetch_youtube_data.py` script retrieves YouTube data and prepares it in the required JSON format.

```python
import requests
import json
from googleapiclient.discovery import build
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "YOUR_PLAYLIST_ID"

def fetch_youtube_playlist_data(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    # Additional logic to fetch video details
    # ...
    return videos

def fetch_youtube_playlist_info(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    # Additional logic to fetch playlist details
    # ...
    return {
        "identifier": playlist_id,
        "blueprint": "youtube_playlist",
        # Additional playlist props
        # ...
    }

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
```
---

   <details>
     <summary>Fetch YouTube Data complete implementation (click to expand)</summary>
     
```python showLineNumbers
import requests
import json
from googleapiclient.discovery import build
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()  # Load environment variables from .env file

# Client credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube playlist details
PLAYLIST_ID = "YOUR_PLAYLIST_ID"

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
            duration = video_details["contentDetails"]["duration"]
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

```
   </details>

---


### Explanation of Workflow Steps

1. **Check out the code**: Retrieves the repository code.
2. **Set up Python**: Configures Python 3.9 environment.
3. **Install dependencies**: Installs required packages from `requirements.txt`.
4. **Run YouTube Data Fetch**: Runs `fetch_youtube_data.py` to retrieve YouTube data and prepare it for Port ingestion.
5. **Bulk Create/Update Entities**: Uses Port’s GitHub action to bulk upsert the playlist and video data.



Here’s an example of what you would see on Port calatog when Playlist and Video data has been injected. 

--- 

<img src='/img/playlist_catalog.png' border='1px' />

---

<img src='/img/playlist_details.png' border='1px' />

---

<img src='/img/videos_catalog.png' border='1px' />

---

<img src='/img/videos_details.png' border='1px' />

---

## Step 3: Visualizing Data in Port

By leveraging Port's Dashboards, you can create custom dashboards to do the following : 

1. A dashboard for tracking playlist-level metrics like the number of videos.
2. Video-level insights, such as view count, position in playlist, and thumbnail displays.

<img src='/img/visualize.png' border='1px' />


### Dashboard setup

1. Go to your [software catalog](https://app.getport.io/organization/catalog).
2. Click on the `+ New` button in the left sidebar.
3. Select **New dashboard**.
4. Name the dashboard ( Visualise Youtube Playlist ), choose an icon if desired, and click `Create`.

This will create a new empty dashboard. Let's get ready-to-add widgets

### Adding widgets

<details>
<summary><b> Count of Videos in Playlist (click to expand)</b></summary>

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Number of Videos`.(add the `Metric` icon).
3. Description: `Shows the number of videos on the playlist`(optional).
4. Select `Count entities` as Chart type.
5. Choose **Youtube Videos** as the **Blueprint**.
6. Select `count` for the **Function**.

<img src="/img/videocounts.png" border="1px" />

8. Click `Save`.

</details>


By following these steps, you can effectively automate the process to catalog YouTube playlist and video data into Port