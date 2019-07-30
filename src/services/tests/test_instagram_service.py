import pytest
from faker import Faker

from config import settings
from services.instagram import InstagramService


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def full_response(fake):
    response_data = {
        'data': {
            'shortcode_media': {
                'edge_media_to_comment': {
                    'page_info': {
                        'has_next_page': False,
                        'end_cursor': None
                    },
                    'edges': []
                }
            }
        },
        'status': 'ok'
    }
    for x in range(20):
        response_data['data']['shortcode_media']['edge_media_to_comment']['edges'].append(
            {
                'node': {
                    'text': fake.pystr()
                }
            }
        )
    return response_data


def test_instagram_service_list_comments(mocker, fake, full_response):

    mocker.patch('instagram_web_api.client.Client.media_comments', return_value=full_response)
    service = InstagramService()
    response = service.list_comments(settings.MEDIA_SHORT_CODE)
    assert len(response) == 20


def test_instagram_service_list_comments_status_not_okay(mocker, fake):
    mocker.patch('instagram_web_api.client.Client.media_comments', return_value={'status': fake.pystr()})
    service = InstagramService()
    response = service.list_comments(settings.MEDIA_SHORT_CODE)
    assert not response


def test_instagram_service_list_comments_with_max_results(mocker, fake, full_response):
    mocker.patch('instagram_web_api.client.Client.media_comments', return_value=full_response)
    service = InstagramService()
    response = service.list_comments(settings.MEDIA_SHORT_CODE, max_comments=10)
    assert len(response) == 10


def test_instagram_service_list_comments_with_key_error(mocker, fake, full_response):
    del full_response['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']
    mocker.patch('instagram_web_api.client.Client.media_comments', return_value=full_response)
    service = InstagramService()
    response = service.list_comments(settings.MEDIA_SHORT_CODE)
    assert not response




