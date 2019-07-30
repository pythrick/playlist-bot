import logging
from typing import List

import requests

from config import settings
from models.media import Media


class YouTubeService:

    API_URL = 'https://www.googleapis.com/youtube/v3/'

    def search_video(self, query: str) -> List[Media]:
        search_url = self.API_URL + 'search'

        search_params = {
            'key': settings.YOUTUBE_API_KEY,
            'part': 'id,snippet',
            'order': 'relevance',
            'q': query,
            'type': 'video',
        }
        try:
            response = requests.get(search_url, params=search_params)
        except Exception as e:
            logging.error(e, exc_info=True)
            raise Exception('YouTube search request failed.')

        try:
            data = response.json()
        except Exception as e:
            logging.error(e, exc_info=True)
            raise Exception("YouTube search didn't return a valid JSON.")

        try:
            return [Media(media_id=item['id']['videoId'], title=item['snippet']['title'])
                    for item in data['items']]
        except (KeyError, TypeError, ValueError) as e:
            logging.error(e, exc_info=True)
            raise Exception("YouTube search didn't return the expected response.")

