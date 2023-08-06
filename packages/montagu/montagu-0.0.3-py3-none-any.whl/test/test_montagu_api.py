from montagu.montagu_api import MontaguAPI
import pytest

base_url = 'http://localhost:8080'
user = 'test.user@example.com'
password = 'password'


def test_init():
    api = MontaguAPI(base_url, user, password)
    assert len(api.token) > 0


def test_error_on_incorrect_credentials():
    with pytest.raises(Exception) as ex:
        MontaguAPI(base_url, user, 'wrong password')
    assert 'Unexpected status code: 401. Unable to authenticate.' \
           in str(ex)


def test_diseases():
    api = MontaguAPI(base_url, user, password)
    diseases = api.diseases()
    assert len(diseases) == 1
    disease = diseases[0]
    assert disease['id'] == 'YF'
    assert disease['name'] == 'Yellow Fever'


def test_error_on_get():
    api = MontaguAPI(base_url, user, password)
    with pytest.raises(Exception) as ex:
        api.get("nonexistent-path")
    assert 'Unexpected status code: 404' in str(ex)
