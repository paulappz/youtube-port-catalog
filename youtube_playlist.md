# YouTube playlist & videos catalog in Port

This guide will help you set up an automated process to catalog YouTube playlist and video data into Port.

Using Port's GitHub action, you’ll fetch YouTube data and ingest it into Port for easy tracking and visualization.

  
## Prerequisites

1. [Create a Port account](https://app.getport.io) and set up API credentials.
2. [Obtain a YouTube Data API Key](https://console.cloud.google.com/apis/credentials).
3. [Set up GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in your repository for:

-  `YOUTUBE_API_KEY`: Your YouTube API key.
-  `CLIENT_ID`: Your Port client ID.
-  `CLIENT_SECRET`: Your Port client secret.

  
## Model data in Port

Data modeling in Port involves defining entities and their relationships to ensure consistent, structured data. 

This step is crucial as it allows your system to understand and manage data efficiently, ensuring that different entities (like playlists and videos) interact seamlessly within workflows.

### Data model setup
1. Navigate to your [Port Builder](https://app.getport.io/settings/data-model) page.
2. Click the `+ Blueprint` button to create a new blueprint.
3. Click the `Edit JSON` button on the modal that appears.
4. Copy and paste the blueprint schemas below into the blueprint editor.


<details>
<summary>Youtube playlist blueprint (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_playlist",
  "title": "YouTube Playlist",
  "icon": "Youtrack",
  "schema": {
    "properties": {
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
    "required": [
      "playlistDescription",
      "publishedAt",
      "channelId",
      "channelTitle"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

</details>

<details>
<summary>Youtube video blueprint (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_video",
  "title": "YouTube Video",
  "icon": "Youtrack",
  "schema": {
    "properties": {
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
    "required": [
      "videoDescription",
      "publishedAt",
      "duration",
      "link"
    ]
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
	<img  src='/img/data_model_blueprints.png'  border='1px'  />
</center>

</details>

## Setup GitHub actions workflow

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

</details>

3. Define workflow in YAML.

<details>
<summary>GitHub workflow (click to expand)</summary>

```yaml showLineNumbers
name: Update YouTube Playlist and Video Entities in Port

on:
  workflow_dispatch:
    inputs:
      playlist_id:
        required: true
        description: "Youtube Playlist Id"
      port_context:
        required: false
        description: |
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
          sudo apt-get install -y jq curl

      - name: Fetch YouTube Video Data
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          PLAYLIST_ID: ${{ github.event.inputs.playlist_id }}
        run: |

          API_KEY="${YOUTUBE_API_KEY}"

          # Fetch playlist details
          playlist_response=$(curl -s "https://youtube.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id=$PLAYLIST_ID&key=$API_KEY")

          # Extract playlist details using jq
          playlist_title=$(echo "$playlist_response" | jq -r '.items[0].snippet.title // "No title available"')
          playlist_description=$(echo "$playlist_response" | jq -r '.items[0].snippet.description // "No description available" | select(length > 0) // "No description available"')
          playlist_published_at=$(echo "$playlist_response" | jq -r '.items[0].snippet.publishedAt // "No published date available"')
          playlist_channel_id=$(echo "$playlist_response" | jq -r '.items[0].snippet.channelId // "No channel ID"')
          playlist_channel_title=$(echo "$playlist_response" | jq -r '.items[0].snippet.channelTitle // "No channel title"')
          playlist_link="https://www.youtube.com/playlist?list=$PLAYLIST_ID"
          playlist_thumbnails_default=$(echo "$playlist_response" | jq -r '.items[0].snippet.thumbnails.default.url // "No thumbnail URL"')
          playlist_thumbnails_medium=$(echo "$playlist_response" | jq -r '.items[0].snippet.thumbnails.medium.url // "No thumbnail URL"')
          playlist_thumbnails_high=$(echo "$playlist_response" | jq -r '.items[0].snippet.thumbnails.high.url // "No thumbnail URL"')
          playlist_thumbnails_standard=$(echo "$playlist_response" | jq -r '.items[0].snippet.thumbnails.standard.url // "No thumbnail URL"')

          # Create playlist JSON
          playlist_json=$(jq -n --arg id "$PLAYLIST_ID" \
                              --arg title "$playlist_title" \
                              --arg link "$playlist_link" \
                              --arg description "$playlist_description" \
                              --arg publishedAt "$playlist_published_at" \
                              --arg channelId "$playlist_channel_id" \
                              --arg channelTitle "$playlist_channel_title" \
                              --arg default_thumbnail "$playlist_thumbnails_default" \
                              --arg medium_thumbnail "$playlist_thumbnails_medium" \
                              --arg high_thumbnail "$playlist_thumbnails_high" \
                              --arg standard_thumbnail "$playlist_thumbnails_standard" \
                              '{
                                  identifier: $id,
                                  blueprint: "youtube_playlist",
                                  title: $title,
                                  description: $description,
                                  properties: {
                                      link: $link,
                                      playlistDescription: $description,
                                      publishedAt: $publishedAt,
                                      channelId: $channelId,
                                      channelTitle: $channelTitle,
                                      thumbnails: {
                                          default: $default_thumbnail,
                                          medium: $medium_thumbnail,
                                          high: $high_thumbnail,
                                          standard: $standard_thumbnail
                                      }
                                  }
                              }')

          # Initialize combined JSON array with the playlist as the first element
          combined_json=$(jq -n --argjson playlist "$playlist_json" '[$playlist]')

          # Pagination setup
          nextPageToken=""

          while true; do
              video_data=$(curl -s "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=10&playlistId=$PLAYLIST_ID&key=$API_KEY&pageToken=$nextPageToken")


              if [ "$(echo $video_data | jq '.items | length')" -eq 0 ]; then
                  echo "No videos found for the playlist."
                  exit 1
              fi

              for video_id in $(echo $video_data | jq -r '.items[].contentDetails.videoId'); do
                  video_response=$(curl -s "https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=$video_id&key=$API_KEY")

                  title=$(echo "$video_response" | jq -r '.items[0].snippet.title')
                  description=$(echo "$video_response" | jq -r '.items[0].snippet.description // "No description available"')
                  publishedAt=$(echo "$video_response" | jq -r '.items[0].snippet.publishedAt')
                  raw_duration=$(echo "$video_response" | jq -r '.items[0].contentDetails.duration')
                  duration=$(echo $raw_duration | sed -E 's/^PT([0-9]+)H([0-9]+)M([0-9]+)S/\1:\2:\3/;s/^PT([0-9]+)M([0-9]+)S/\1:\2/;s/^PT([0-9]+)H([0-9]+)M/\1:\2/;s/^PT([0-9]+)M/\1:00/;s/^PT([0-9]+)H/\1:00:00/' | sed 's/^://')
                  likes=$(echo "$video_response" | jq -r '.items[0].statistics.likeCount // 0')
                  views=$(echo "$video_response" | jq -r '.items[0].statistics.viewCount // 0')
                  comments=$(echo "$video_response" | jq -r '.items[0].statistics.commentCount // 0')
                  link="https://www.youtube.com/watch?v=$video_id"

                  videoOwnerChannelTitle=$(echo "$video_response" | jq -r '.items[0].snippet.channelTitle // "No channel title"')
                  videoOwnerChannelId=$(echo "$video_response" | jq -r '.items[0].snippet.channelId // "No channel ID"')

                  video_thumbnails_default=$(echo "$video_response" | jq -r '.items[0].snippet.thumbnails.default.url // "No thumbnail URL"')
                  video_thumbnails_medium=$(echo "$video_response" | jq -r '.items[0].snippet.thumbnails.medium.url // "No thumbnail URL"')
                  video_thumbnails_high=$(echo "$video_response" | jq -r '.items[0].snippet.thumbnails.high.url // "No thumbnail URL"')
                  video_thumbnails_standard=$(echo "$video_response" | jq -r '.items[0].snippet.thumbnails.standard.url // "No thumbnail URL"')

                  position=$(echo "$video_data" | jq -r --arg video_id "$video_id" '.items[] | select(.contentDetails.videoId == $video_id) | .snippet.position')

                  video_json=$(jq -n \
                      --arg id "$video_id" \
                      --arg title "$title" \
                      --arg link "$link" \
                      --arg description "$description" \
                      --arg publishedAt "$publishedAt" \
                      --arg duration "$duration" \
                      --arg likes "$likes" \
                      --arg views "$views" \
                      --arg comments "$comments" \
                      --arg position "$position" \
                      --arg playlist_id "$PLAYLIST_ID" \
                      --arg videoOwnerChannelTitle "$videoOwnerChannelTitle" \
                      --arg videoOwnerChannelId "$videoOwnerChannelId" \
                      --arg video_thumbnails_default "$video_thumbnails_default" \
                      --arg video_thumbnails_medium "$video_thumbnails_medium" \
                      --arg video_thumbnails_high "$video_thumbnails_high" \
                      --arg video_thumbnails_standard "$video_thumbnails_standard" \
                      '{
                        identifier: $id,
                        blueprint: "youtube_video",
                        title: $title,
                        properties: {
                          link: $link,
                          videoDescription: $description,
                          publishedAt: $publishedAt,
                          duration: $duration,
                          likes: $likes,
                          views: $views,
                          comments: $comments,
                          position: $position,
                          videoOwnerChannelTitle: $videoOwnerChannelTitle,
                          videoOwnerChannelId: $videoOwnerChannelId,
                          thumbnails: {
                            default: $video_thumbnails_default,
                            medium: $video_thumbnails_medium,
                            high: $video_thumbnails_high,
                            standard: $video_thumbnails_standard
                          }
                        },
                        relations: {
                          playlist: $playlist_id
                        }
                      }')

                  echo "Processed video JSON: $video_json"

                  combined_json=$(echo $combined_json | jq --argjson video "$video_json" '. + [$video]')
              done

              nextPageToken=$(echo $video_data | jq -r '.nextPageToken')
              if [ "$nextPageToken" == "null" ]; then
                  break
              fi
          done

          echo $combined_json > port_entities.json
          echo "entities=$(jq -c . port_entities.json)" >> $GITHUB_ENV

      - name: Bulk Create/Update YouTube Playlist and Video Entities in Port
        id: bulk_create_update
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
          status: ${{ steps.bulk_create_update.outcome == 'success' && 'SUCCESS' || 'FAILURE' }}
          runId: ${{fromJson(inputs.port_context).runId}}
          logMessage: ${{ steps.bulk_create_update.outcome == 'success' && 'YouTube Data created/Updated Successfully' || 'Error in YouTube Data creation/update' }}  
```

</details>

4. Add and push the workflow file to your repository.
  

## Create self-service actions for YouTube playlist

Self-service actions in Port allow developers to perform tasks like scaffolding a service or provisioning a cloud resource through an intuitive UI.

#### How it works

1.  **User Executes Action**: A user triggers an action from Port's UI.
2.  **Payload Sent**: A payload with metadata and inputs is sent to your infrastructure.
3.  **Job Triggered**: A job runs, and the user receives continuous progress updates.
4.  **Update Port**: The action's status, logs, and links are sent back to Port.

#### Guide to create a self-service action for YouTube playlist workflow

1. Navigate to the Self-service page and click the `+ New Action` button.
2. Click the `Edit JSON` button on the modal that appears.
3. Copy and paste the self-service action JSON (seen below) in the JSON section.

<details>

<summary> Self-service action JSON: (click to expand)</summary>

```json
{
  "identifier": "create_youtube_catalog",
  "title": "Create Youtube Catalog",
  "icon": "Github",
  "description": "Self Service Action for Youtube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "playlist_id": {
          "icon": "DefaultProperty",
          "title": "Youtube Playlist Id",
          "type": "string"
        }
      },
      "required": [
        "playlist_id"
      ]
    },
    "blueprintIdentifier": "youtube_playlist"
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "your-github-org",
    "repo": "your-github-repo",
    "workflow": "your-workflow-file.yml",
    "workflowInputs": {
      "{{ spreadValue() }}": "{{ .inputs }}",
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

</details>


4. Click `Save`.
5. Click  `Create` button on just created action on the self service action page.
6. Enter the Playlist Id in the input feild. 
7. Click  the `Execute` button to execute the action.

  <details>
  <summary> Execute action (click to expand)</summary>
  <center>
    <img  src='/img/selfservice_action.png'  border='1px'  />
  </center>

  </details>

8. Click  `My inprogress run` to see the action status.

  <details>

  <summary> Action in progress (click to expand)</summary>
  <center>
    <img  src='/img/portaction.png'  border='1px'  />
  </center>

  </details>

9. Go to **Actions** tab in GitHub to see workflow execution.
  
  <details>

  <summary> GitHub action (click to expand)</summary>
  <center>
    <img  src='/img/github_action.png'  border='1px'  />
  </center>

  </details>


<details>

<summary>Here’s an example of what you would see on Port calatog when playlist and video data have been ingested. (click to expand)</summary>

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

  
## Visualizing data in Port

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

### Creating a dashboard in Port

If you followed through with the dashboard setup, you will have created a new empty dashboard as seen in the last image. Let's get ready to add widgets.

### Adding widgets

Let's create a widget that displays the number of videos in a YouTube playlist.

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Number of Videos`. (add the `Metric` icon).
3. Description: `Shows the number of videos on the playlist` (optional).
4. Select `Count entities` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `count` for the **Function**.  
7. Click `Save`.

<details>
<summary><b>Count of videos in playlist (click to expand)</b></summary>
    <center>
    <img src="/img/video_counts.png" border="1px" />
    </center>
</details>

#### Creating other widgets

You can also create other widgets to display additional data about your YouTube videos such as:

**Average number of likes across all videos**

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Average Likes`. (add the `Metric` icon).
3. Description: `Shows the average number of likes across all videos` (optional).
4. Select `Agregate by property` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `Like Count` for the **Property**.
6. Select `Average` for the **Function**.
7. Select `total` for the **Average of**.
8. Click `Save`.

<details>
<summary><b>Average number of likes (click to expand)</b></summary>
    <center>
    <img src="/img/average_likes.png" border="1px" />
    </center>
</details>

**Number of views a video has**

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Total Views`. (add the `Metric` icon).
3. Description: `Shows the total number of views for all videos` (optional).
4. Select `Agregate by property` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `View Count` for the **Property**.
7. Select `Sum` for the **Function**.
8. Click `Save`.

<details>
<summary><b>Number of views (click to expand)</b></summary>
    <center>
    <img src="/img/total_views.png" border="1px" />
    </center>
</details>

By following these steps, you can effectively automate the process to catalog YouTube playlist and video data into Port.