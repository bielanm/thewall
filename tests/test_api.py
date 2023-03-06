import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_app_status(client):
    url = '/profiles/setup'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json().get('setup') == False