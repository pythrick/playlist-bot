import pytest
from faker import Faker

from models.media import Media


@pytest.fixture
def fake():
    return Faker()


def test_media_model(fake):
    media = Media(
        media_id=fake.pystr(),
        title=fake.pystr(),
        description=fake.pystr()
    )
    assert str(media) == media.title
    assert repr(media) == f'{media.media_id}: {media.title}'
