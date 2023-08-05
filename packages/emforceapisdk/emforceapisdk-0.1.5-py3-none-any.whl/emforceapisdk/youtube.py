#!/usr/bin/python
from apiclient import discovery


class Youtube:
    def __init__(self, developer_key=None):
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = discovery.build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                                       developerKey=developer_key)

    def video_category_list(self, region_code="KR"):
        res = self.youtube.videoCategories().list(
            part="id,snippet",
            regionCode=region_code
        ).execute()

        return_data = []

        items = res.get('items', None)
        for item in items:
            return_data.append({
                "id": item.get("id"),
                "etag": item.get("etag"),
                "title": item.get('snippet').get('title'),
                "channelId": item.get('snippet').get('channelId')
            })

        return return_data

    def most_popular_video_list(self, max_result=50, page_token=None):
        video_list = self.youtube.videos().list(
            part='id,snippet, statistics',
            chart='mostPopular',
            regionCOde='KR',
            pageToken=page_token,
            maxResults=max_result
        )

        return_data = []

        for video in video_list:
            return_data.append({
                "id": video['id'],
                "publishedAt": video['snippet']['publishedAt'],
                "channelId": video['snippet']['channelId'],
                "channelTitle": video['snippet']['channelTitle'],
                "title": video['snippet']['title'],
                "description": video['snippet']['description'],
                "thumbnails": video['snippet']['thumbnails'],
                "tags": video['snippet']['tags'],

                "categoryId": video['snippet']['categoryId'],
                "liveBroadcastContent": video['snippet']['liveBroadcastContent'],
                "defaultAudioLanguage": video['snippet']['defaultAudioLanguage'],

                "viewCount": video['statistics']['viewCount'],
                "likeCount": video['statistics']['likeCount'],
                "dislikeCount": video['statistics']['dislikeCount'],
                "favoriteCount": video['statistics']['favoriteCount'],
                "commentCount": video['statistics']['commentCount'],

            })

        return return_data

    def channel_detail(self, id):
        channel_detaill = self.youtube.videos().list(
            q=id,
            part='id,snippet,statistics,topicDetails'
        )

        return_data = {
            "id": channel_detaill['id'],
            "title": channel_detaill['snippet']['title'],
            "description": channel_detaill['snippet']['description'],
            "publishedAt": channel_detaill['snippet']['publishedAt'],
            "thumbnails": channel_detaill['snippet']['thumbnails'],
            "localized": channel_detaill['snippet']['localized'],
            "country": channel_detaill['snippet']['country'],
            "viewCount": channel_detaill['statistics']['viewCount'],
            "subscriberCount": channel_detaill['statistics']['subscriberCount'],
            "videoCount": channel_detaill['statistics']['videoCount'],
            "commentCount": channel_detaill['statistics']['commentCount'],
            "topicIds": channel_detaill['topicDetails']['topicIds'],
            "topicCategories": channel_detaill['topicDetails']['topicCategories'],
        }

        return return_data

    def search(self, keyword, max_result=50, page_token=None):
        search_response = self.youtube.search().list(
            q=keyword,
            part="id,snippet",
            pageToken=page_token,
            maxResults=max_result
        ).execute()

        videos = []
        channels = []
        playlists = []

        pageInfo = search_response.get('pageInfo')
        prevPageToken = search_response.get('prevPageToken')
        nextPageToken = search_response.get('nextPageToken')
        pageInfo['prevPageToken'] = prevPageToken
        pageInfo['nextPageToken'] = nextPageToken

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append({
                    "etag": search_result['etag'],
                    "vedioId": search_result["id"]["videoId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "channelId": search_result["snippet"]["channelId"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "title": search_result["snippet"]["title"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],

                })
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append({
                    "etag": search_result['etag'],
                    "channelId": search_result["id"]["channelId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],
                })
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append({
                    "etag": search_result['etag'],
                    "playlistId": search_result["id"]["playlistId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "channelId": search_result["snippet"]["channelId"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],
                })

        return_data = {
            "page_info": pageInfo,
            "videos": videos,
            "channels": channels,
            "playlists": playlists
        }

        return return_data
