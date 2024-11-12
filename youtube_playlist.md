
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


### Create a Port action using the following JSON definition:

```yaml showLineNumbers
{
  "identifier": "create_youtube_catalog",
  "title": "Create Youtube Catalog",
  "icon": "Github",
  "description": "Automate Youtube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "  Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    },
    "blueprintIdentifier": "youtubecatalog"
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "paulappz",
    "repo": "port-documentation",
    "workflow": "port-youtube-ingest.yml",
    "workflowInputs": {
      "port_context": {
        "entity": "{{.entity}}",
        "blueprint": "{{.action.blueprint}}",
        "runId": "{{.run.id}}",
        "trigger": "{{ .trigger }}"
      }
    },
    "reportWorkflowStatus": true
  },
  "requiredApproval": false
}
```

--- 

<img src='/img/catalogblueprint.png' border='1px' />

---

###  Create a Port action using the following JSON definition:

```yaml
{
  "identifier": "create_youtube_catalog",
  "title": "Create Youtube Catalog",
  "icon": "Github",
  "description": "Automate Youtube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "  Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    },
    "blueprintIdentifier": "youtubecatalog"
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "paulappz",
    "repo": "port-documentation",
    "workflow": "port-youtube-ingest.yml",
    "workflowInputs": {
      "port_context": {
        "entity": "{{.entity}}",
        "blueprint": "{{.action.blueprint}}",
        "runId": "{{.run.id}}",
        "trigger": "{{ .trigger }}"
      }
    },
    "reportWorkflowStatus": true
  },
  "requiredApproval": false
}
```

---

<img src='/img/portaction.png' border='1px' />

---


The following GitHub workflow automates fetching data from YouTube and updating Port with the data.

### GitHub Workflow (`.github/workflows/youtube_port_workflow.yml`)

<details>
<summary><b>

```yaml showLineNumbers
name: Update YouTube Playlist and Video Entities in Port

on:
  workflow_dispatch:
    inputs:
      port_context:
        required: false
        description:
          Who triggered the action and general context (blueprint, run id, etc...)
        type: string 

jobs:
  update_port_entities:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v2

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y jq

      - name: Fetch YouTube Playlist and Video Data
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: |
          PLAYLIST_ID="PL5ErBr2d3QJH0kbwTQ7HSuzvBb4zIWzhy"
          
          # Fetch playlist details
          playlist_response=$(curl -s "https://youtube.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id=$PLAYLIST_ID&key=$YOUTUBE_API_KEY")
          playlist_title=$(echo $playlist_response | jq -r '.items[0].snippet.title')
          playlist_description=$(echo $playlist_response | jq -r '.items[0].snippet.description // "No description available"')
          playlist_published_at=$(echo $playlist_response | jq -r '.items[0].snippet.publishedAt')
          playlist_channel_id=$(echo $playlist_response | jq -r '.items[0].snippet.channelId')
          playlist_channel_title=$(echo $playlist_response | jq -r '.items[0].snippet.channelTitle')
          playlist_link="https://www.youtube.com/playlist?list=$PLAYLIST_ID"

          # Save playlist data in JSON format compatible with Port
          playlist_json=$(jq -n --arg id "$PLAYLIST_ID" \
                              --arg title "$playlist_title" \
                              --arg link "$playlist_link" \
                              --arg description "$playlist_description" \
                              --arg publishedAt "$playlist_published_at" \
                              --arg channelId "$playlist_channel_id" \
                              --arg channelTitle "$playlist_channel_title" \
                              '{
                                identifier: $id,
                                blueprint: "youtube_playlist",
                                title: $title,
                                properties: {
                                  title: $title,
                                  link: $link,
                                  description: $description,
                                  publishedAt: $publishedAt,
                                  channelId: $channelId,
                                  channelTitle: $channelTitle
                                }
                              }')

          # Initialize combined JSON array with the playlist as the first element
          combined_json=$(jq -n --argjson playlist "$playlist_json" '[$playlist]')

          # Fetch video details for each video in the playlist
          video_data=$(curl -s "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=10&playlistId=$PLAYLIST_ID&key=$YOUTUBE_API_KEY")

          # Function to convert ISO 8601 duration to H:MM:SS format
          convert_duration() {
            local duration=$1
            local hours=$(echo $duration | grep -oP '(?<=PT)(\d+)H' | grep -oP '\d+')
            local minutes=$(echo $duration | grep -oP '(?<=T|\d)M' | grep -oP '\d+')
            local seconds=$(echo $duration | grep -oP '(?<=M|\d)S' | grep -oP '\d+')
            printf "%s:%02d:%02d" "${hours:-0}" "${minutes:-0}" "${seconds:-0}"
          }

          # Loop through each video, gather details, and format JSON for Port
          for video_id in $(echo $video_data | jq -r '.items[].contentDetails.videoId'); do
            video_response=$(curl -s "https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=$video_id&key=$YOUTUBE_API_KEY")

            title=$(echo $video_response | jq -r '.items[0].snippet.title')
            description=$(echo $video_response | jq -r '.items[0].snippet.description // "No description available"')
            publishedAt=$(echo $video_response | jq -r '.items[0].snippet.publishedAt')
            raw_duration=$(echo $video_response | jq -r '.items[0].contentDetails.duration')
            duration=$(convert_duration $raw_duration)
            likes=$(echo $video_response | jq -r '.items[0].statistics.likeCount // 0')
            views=$(echo $video_response | jq -r '.items[0].statistics.viewCount // 0')
            comments=$(echo $video_response | jq -r '.items[0].statistics.commentCount // 0')
            link="https://www.youtube.com/watch?v=$video_id"

            video_json=$(jq -n --arg id "$video_id" \
                               --arg title "$title" \
                               --arg link "$link" \
                               --arg description "$description" \
                               --arg publishedAt "$publishedAt" \
                               --arg duration "$duration" \
                               --arg likes "$likes" \
                               --arg views "$views" \
                               --arg comments "$comments" \
                               --arg playlist_id "$PLAYLIST_ID" \
                               '{
                                 identifier: $id,
                                 blueprint: "youtube_video",
                                 title: $title,
                                 properties: {
                                   title: $title,
                                   link: $link,
                                   description: $description,
                                   publishedAt: $publishedAt,
                                   duration: $duration,
                                   likes: $likes,
                                   views: $views,
                                   comments: $comments
                                 },
                                 relations: {
                                   playlist: $playlist_id
                                 }
                               }')

            # Append each video JSON to the combined JSON array
            combined_json=$(echo $combined_json | jq --argjson video "$video_json" '. + [$video]')
          done

          # Save the combined JSON array to the environment variable for Port
          echo $combined_json > port_entities.json
          echo "entities=$(jq -c . port_entities.json)" >> $GITHUB_ENV

      - name: Bulk Create/Update YouTube Playlist and Video Entities in Port
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.PORT_CLIENT_ID }}
          clientSecret: ${{ secrets.PORT_CLIENT_SECRET }}
          baseUrl: https://api.getport.io
          operation: BULK_UPSERT
          entities: ${{ env.entities }}

      - name: Inform completion of request to Create / Update Catalog in Port
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.PORT_CLIENT_ID }}
          clientSecret: ${{ secrets.PORT_CLIENT_SECRET }}
          baseUrl: https://api.getport.io
          operation: PATCH_RUN
          status: "SUCCESS"
          runId: ${{fromJson(inputs.port_context).runId}}
          logMessage: "Created github secret ${{ github.event.inputs.secret_key }}"
```

</details>

---



### Explanation of Workflow Steps

1. **Create YouTube Catalog Automation Blueprint in Port**: This blueprint sets up the Port cataloging process to automate playlist and video ingestion.
2. **Check out the code**: Retrieves the repository code from GitHub.
3. **Install dependencies**: Installs `jq`, a tool for JSON processing, to handle YouTube API responses directly in the workflow.
4. **Fetch YouTube Data and Prepare for Port**: Uses `curl` to retrieve YouTube playlist and video data, parses the data using `jq`, and converts it into JSON format compatible with Port’s data model.
5. **Bulk Create/Update Entities**: Uses Port’s GitHub action to bulk upsert the combined playlist and video data into Port.
6. **Inform Completion**: Sends a `PATCH_RUN` operation back to Port to mark the workflow as completed with a `SUCCESS` status, including a log message for tracking purposes.



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