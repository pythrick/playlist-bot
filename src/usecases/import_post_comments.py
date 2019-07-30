from config import settings
from services import InstagramService


class ImportPostComments():
    def __call__(self, *args, **kwargs):
        instagram_service = InstagramService()
        comments = instagram_service.list_comments(settings.MEDIA_SHORT_CODE)
        return comments
