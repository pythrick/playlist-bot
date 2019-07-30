import pytest
from faker import Faker

from usecases import ImportPostComments


@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def comments_list(fake):
    return [fake.pystr() for _ in range(10)]


def test_import_post_comments(mocker, comments_list):
    mocker.patch('services.instagram.InstagramService.list_comments', return_value=comments_list)
    usecase = ImportPostComments()
    result = usecase()
    assert len(result) == 10
