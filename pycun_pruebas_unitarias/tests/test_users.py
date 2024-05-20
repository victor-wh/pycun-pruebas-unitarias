import pytest

from pycun_pruebas_unitarias.apps.users.views import login


# Create your tests here.
def test_login_pass():
    login_passes = login("uskokrum2010", "123456")
    assert login_passes


def test_login_fail():
    login_fails = login("uskokrum2010XD", "12345678")
    assert not login_fails
