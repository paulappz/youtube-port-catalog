This guide will help you set up an automated process to catalog YouTube playlist and video data into Port.

Using Port's GitHub action, you’ll fetch YouTube data and ingest it into Port for easy tracking and visualization.

  
## Prerequisites

1. [Create a Port account](https://app.getport.io) and set up API credentials.
2. [Obtain a YouTube Data API Key](https://console.cloud.google.com/apis/credentials).
3. [Set up GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in your repository for:

-  `YOUTUBE_API_KEY`: Your YouTube API key.
-  `CLIENT_ID`: Your Port client ID.
-  `CLIENT_SECRET`: Your Port client secret.

  
## Step 1: Model Data in Port

### Data model setup
1. Navigate to your [Port Builder](https://app.getport.io/settings/data-model) page.
2. Click the `+ Blueprint` button to create a new blueprint.
3. Click the Edit JSON button on the Modal and

<details>
	<summary>Example of blueprint for `youtube_video` created (click to expand)	</summary>

<center>
	<img  src='/img/blueprint.png'  border='1px'  />
</center>

</details>

4. Add the Deployment blueprints in JSON format.

<details>
<summary>Deployment blueprint for `youtube_playlist` (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_playlist",
  "title": "YouTube Playlist",
  "description": "Blueprint for YouTube Playlist",
  "icon": "YouTube",
  "schema": {
    "properties": {
      "playlistTitle": {
        "type": "string",
        "title": "Playlist Title",
        "description": "The title of the YouTube playlist."
      },
      "link": {
        "type": "string",
        "title": "Playlist Link",
        "format": "url",
        "description": "The URL link to the YouTube playlist."
      },
      "playlistDescription": {
        "type": "string",
        "title": "Playlist Description",
        "description": "A detailed description of the YouTube playlist."
      },
      "publishedAt": {
        "type": "string",
        "title": "Publish Date",
        "format": "date-time",
        "description": "The date and time when the playlist was published."
      },
      "channelId": {
        "type": "string",
        "title": "Channel ID",
        "description": "The ID of the YouTube channel that owns the playlist."
      },
      "channelTitle": {
        "type": "string",
        "title": "Channel Title",
        "description": "The title of the YouTube channel that owns the playlist."
      },
      "thumbnails": {
        "type": "object",
        "title": "Thumbnails",
        "description": "Various resolution thumbnails for the playlist.",
        "properties": {
          "default": {
            "type": "string",
            "title": "Default Thumbnail",
            "description": "URL for the default thumbnail image."
          },
          "medium": {
            "type": "string",
            "title": "Medium Thumbnail",
            "description": "URL for the medium-sized thumbnail image."
          },
          "high": {
            "type": "string",
            "title": "High Thumbnail",
            "description": "URL for the high-resolution thumbnail image."
          },
          "standard": {
            "type": "string",
            "title": "Standard Thumbnail",
            "description": "URL for the standard thumbnail image."
          }
        }
      },
      "localized": {
        "type": "object",
        "title": "Localized Information",
        "description": "Localized title and description for different regions.",
        "properties": {
          "title": {
            "type": "string",
            "title": "Localized Title",
            "description": "The localized title of the playlist."
          },
          "description": {
            "type": "string",
            "title": "Localized Description",
            "description": "The localized description of the playlist."
          }
        }
      }
    },
    "required": ["playlistTitle", "playlistDescription", "publishedAt", "channelId", "channelTitle"]    
    },    
    "mirrorProperties": {},
    "calculationProperties": {},
    "aggregationProperties": {},
    "relations": {}
  }

```

</details>

<details>
<summary>Deployment blueprint for `youtube_video` (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_video",
  "title": "YouTube Video",
  "description": "Blueprint for YouTube Video",
  "icon": "YouTube",
  "schema": {
    "properties": {
      "videoTitle": {
        "type": "string",
        "title": "Video Title",
        "description": "The title of the YouTube video."
      },
      "link": {
        "type": "string",
        "title": "Video Link",
        "format": "url",
        "description": "The URL link to the YouTube video."
      },
      "duration": {
        "type": "string",
        "title": "Video Duration",
        "description": "The duration of the YouTube video."
      },
      "videoDescription": {
        "type": "string",
        "title": "Video Description",
        "description": "A detailed description of the YouTube video."
      },
      "publishedAt": {
        "type": "string",
        "title": "Publish Date",
        "format": "date-time",
        "description": "The date and time when the video was published."
      },
      "position": {
        "type": "number",
        "title": "Position in Playlist",
        "description": "The video's position in the playlist."
      },
      "likes": {
        "type": "number",
        "title": "Like Count",
        "description": "The number of likes on the video."
      },
      "views": {
        "type": "number",
        "title": "View Count",
        "description": "The number of views on the video."
      },
      "comments": {
        "type": "number",
        "title": "Comment Count",
        "description": "The number of comments on the video."
      },
      "thumbnails": {
        "type": "object",
        "title": "Thumbnails",
        "description": "Various resolution thumbnails for the video.",
        "properties": {
          "default": {
            "type": "string",
            "title": "Default Thumbnail",
            "description": "URL for the default thumbnail image."
          },
          "medium": {
            "type": "string",
            "title": "Medium Thumbnail",
            "description": "URL for the medium-sized thumbnail image."
          },
          "high": {
            "type": "string",
            "title": "High Thumbnail",
            "description": "URL for the high-resolution thumbnail image."
          },
          "standard": {
            "type": "string",
            "title": "Standard Thumbnail",
            "description": "URL for the standard thumbnail image."
          },
          "maxres": {
            "type": "string",
            "title": "Max Resolution Thumbnail",
            "description": "URL for the maximum resolution thumbnail image."
          }
        }
      },
      "videoOwnerChannelTitle": {
        "type": "string",
        "title": "Channel Title",
        "description": "The title of the channel that owns the video."
      },
      "videoOwnerChannelId": {
        "type": "string",
        "title": "Channel ID",
        "description": "The ID of the channel that owns the video."
      }
    },
    "required": ["videoTitle", "videoDescription", "publishedAt", "duration", "link"]
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

<center>
	<img  src='/img/data_model.png'  border='1px'  />
</center>

</details>

  
## Step 2: GitHub Workflow for Data Ingestion


### Create a Youtube Catalog Blueprint using JSON definition.

<details>

<summary>Deployment blueprint for `Youtube Catalog` Action (click to expand)</summary>

```yaml showLineNumbers
{
  "identifier": "youtubecatalog",
  "title": "YouTubeCatalogAutomation",
  "icon": "Github",
  "schema": {
    "properties": {
      "service_name": {
        "icon": "Github",
        "title": "Service Name",
        "type": "string",
        "description": "All Uppercase"
      }
    },
    "required": [
      "service_name"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}

```

<center>
	<img  src='/img/catalogblueprint.png'  border='1px'  />
</center>

</details>

 
### Create Self-service Actions

Self-service actions in Port allow developers to perform tasks like scaffolding a service or provisioning a cloud resource through an intuitive UI.

#### How It Works

1.  **User Executes Action**: A user triggers an action from Port's UI.

2.  **Payload Sent**: A payload with metadata and inputs is sent to your infrastructure.

3.  **Job Triggered**: A job runs, and the user receives continuous progress updates.

4.  **Update Port**: The action's status, logs, and links are sent back to Port.

#### Step-by-Step Guide to create a Self-service Action for Youtube Playlist Workflow.

1. Navigate to the Self-service page and click the + New Action button.
2. Choose a name and icon for the action.
3. Define the inputs users need to fill out when executing the action.

  
**Action's Frontend:**

<details>
<summary>Self service action frontend (click to expand)</summary>

```json

  {
  "identifier": "create_youtube_catalog",
  "title": "Create YouTube Catalog",
  "icon": "Github",
  "description": "Self Service Action for YouTube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    }
  }
}
```

</details>


**Define Action's Backend**

1. Define an **Invocation Method** of type **GITHUB** to define how the action will be executed.

2. Specify the payload to be sent to your handler.

<details>
<summary> Self service action backend (click to expand)</summary>

```json
{
  "invocationMethod": {
    "type": "GITHUB",
    "org": "your-github-org",
    "repo": "your-github-repo",
    "workflow": "your-workflow-file.yml",
    "workflowInputs": {
      "port_context": {
        "entity": "{{.entity}}",
        "blueprint": "{{.action.blueprint}}",
        "runId": "{{.run.id}}",
        "trigger": "{{ .trigger }}"
      }
    },
    "reportWorkflowStatus": true
  }
}
```

</details>

**Set Guardrails (Optional)**

Manual Approvals: We instruct to set Manual approval while needed. but we will setup to false in this case.  

<details>
<summary>Manual approval congiration (click to expand)</summary>

```json
{
  "requiredApproval": false
}
```
</details>

 
**Execute the Action**

Users can execute the action from the Port UI.

<details>

<summary>Self service action execution (click to expand)</summary>

```json
{
  "status": "SUCCESS",
  "logMessage": "YouTube Data created/Updated",
  "links": [
    {
      "name": "GitHub Workflow",
      "url": "https://github.com/your-github-org/your-github-repo/actions/runs/123456789"
    }
  ]
}
```

</details>

#### Action JSON Structure

<details>

<summary> Here is a basic structure of a self-service action: (click to expand)</summary>

```json


{
  "identifier": "create_youtube_catalog",
  "title": "Create YouTube Catalog",
  "icon": "Github",
  "description": "Automate YouTube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    }
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "your-github-org",
    "repo": "your-github-repo",
    "workflow": "your-workflow-file.yml",
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

<center>

  <img  src='/img/portaction.png'  border='1px'  />

</center>

</details>
  
The following GitHub workflow automates fetching data from YouTube and updating Port with the data.


# GitHub Actions Workflow Guide

1. Create `.github/workflows` in your repository.

2. Inside `.github/workflows`, create a YAML file (e.g., `youtube_port_workflow.yml`).

<details>

<summary>Example (click to expand)</summary>

```

<repository-root>/

      └── .github/

          └── workflows/

              └── <workflow-file>.yml

```

<details>

3. Define Workflow in YAML

<details>
<summary>GitHub Workflow (click to expand)</summary>

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
                                description: $description,
                                properties: {
                                  playlistTitle: $title,
                                  link: $link,
                                  playlistDescription: $description,
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
                                 description:$title
                                 properties: {
                                   videoTitle: $title,
                                   link: $link,
                                   videoDescription: $description,
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
          logMessage: "Youtube Data created/Updated Successfully"
```

</details>


4. Add and push the workflow file to your repository.

5. Go to **Actions** tab in GitHub to see workflow execution.

6. Go to **Settings** > **Secrets** to add Secrets usedin the workflow.

  
<details>

<summary>Here’s an example of what you would see on Port calatog when Playlist and Video data has been injected. (click to expand)</summary>

<center>
<img  src='/img/playlist_catalog.png'  border='1px'  />
</center>
<center>
<img  src='/img/playlist_details.png'  border='1px'  />
</center>
<center>
<img  src='/img/videos_catalog.png'  border='1px'  />
</center>
<center>
<img  src='/img/videos_details.png'  border='1px'  />
</center>
</details>

  
## Step 3: Visualizing Data in Port

By leveraging Port's Dashboards, you can create custom dashboards to do the following :
1. A dashboard for tracking playlist-level metrics like the number of videos.
2. Video-level insights, such as view count, position in playlist, and thumbnail displays.

<details>

<summary> Here’s an example of what you would see (click to expand)</summary>

<center>
<img  src='/img/visualize.png'  border='1px'  />
</center>
 
</details>


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

<center>
<img  src="/img/videocounts.png"  border="1px"  />
</center>
  
8. Click `Save`.

</details>

  
By following these steps, you can effectively automate the process to catalog YouTube playlist and video data into Port