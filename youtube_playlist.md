
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
    "repo": "port-doc",
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
    "repo": "port-doc",
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

```yaml showLineNumbers

```

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