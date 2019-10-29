import hashlib
import string
import random
import time

from typing import List

from instagram_web_api import Client


class InstagramService(Client):
    def __init__(self):
        super(InstagramService, self).__init__(auto_patch=False, drop_incompat_keys=False)

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())

    @staticmethod
    def _delay() -> None:
        time.sleep(random.uniform(1, 5))
        return None

    def list_comments(self, post_short_code: str, max_comments: int = None) -> List['str']:
        comments = []
        end_cursor = None
        has_next_page = True
        while has_next_page:
            result = self.media_comments(post_short_code, count=50, end_cursor=end_cursor, extract=False)
            if not isinstance(result, dict) or result.get('status') != 'ok':
                return comments
            try:
                has_next_page = result['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']
                end_cursor = result['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
                for c in result['data']['shortcode_media']['edge_media_to_comment']['edges']:
                    comments.append(c['node']['text'])
                    if max_comments and len(comments) == max_comments:
                        return comments
            except KeyError:
                return comments

            self._delay()
        return comments
