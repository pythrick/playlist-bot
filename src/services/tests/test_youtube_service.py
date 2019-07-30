from dataclasses import dataclass

import pytest
from faker import Faker

from models.media import Media
from services import YouTubeService


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def valid_search_video_response(fake):
    @dataclass
    class MockResponse:
        status_code: int = 200

        def json(self):
            items = [{
                        'id': {'videoId': fake.pystr()},
                        'snippet': {
                            'title': fake.pystr()
                        }
                    } for _ in range(10)]
            return {'items': items}

    return MockResponse()


def test_youtube_service_search_video(mocker, fake, valid_search_video_response):
    service = YouTubeService()
    query = fake.pystr()
    mocker.patch('requests.get', return_value=valid_search_video_response)
    result = service.search_video(query)
    assert len(result) == 10
    assert isinstance(result[0], Media)
    assert isinstance(result[0].media_id, str)
    assert isinstance(result[0].title, str)


def test_youtube_service_search_video_raising_exeption(mocker, fake):
    service = YouTubeService()
    query = fake.pystr()
    with mocker.patch('requests.get', side_effect=Exception('Request failed.')):
        with pytest.raises(Exception) as e:
            assert service.search_video(query)
    assert str(e.value) == 'YouTube search request failed.'


def test_youtube_service_search_video_invalid_json(mocker, fake, valid_search_video_response):
    valid_search_video_response.json = Exception(fake.pystr())

    service = YouTubeService()
    query = fake.pystr()
    mocker.patch('requests.get', return_value=valid_search_video_response)
    with pytest.raises(Exception) as e:
        assert service.search_video(query)
    assert str(e.value) == "YouTube search didn't return a valid JSON."


def test_youtube_service_search_video_invalid_data_response(mocker, fake):
    @dataclass
    class MockResponse:
        status_code: int = 200

        @staticmethod
        def json():
            return fake.pydict()

    service = YouTubeService()
    query = fake.pystr()
    mocker.patch('requests.get', return_value=MockResponse())
    with pytest.raises(Exception) as e:
        assert service.search_video(query)
    assert str(e.value) == "YouTube search didn't return the expected response."
