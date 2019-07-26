import hashlib
import string
import random
from typing import List

from instagram_web_api import Client

import settings


class MyClient(Client):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())


web_api = MyClient(auto_patch=False, drop_incompat_keys=False)


def get_comments(max_comments: int = None) -> List['str']:
    texts = []
    end_cursor = None
    has_next_page = True
    while has_next_page:
        result = web_api.media_comments(settings.MEDIA_SHORT_CODE, count=50, end_cursor=end_cursor, extract=False)
        if not isinstance(result, dict) or result.get('status') != 'ok':
            return texts
        try:
            has_next_page = result['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']
            end_cursor = result['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
            for c in result['data']['shortcode_media']['edge_media_to_comment']['edges']:
                texts.append(c['node']['text'])
                if max_comments and len(texts) == max_comments:
                    return texts
        except KeyError:
            return texts
    return texts
