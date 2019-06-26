# pylint: disable=redefined-outer-name
"""Tests for examples/app.y"""
import json
import pytest
from falcon import testing
import examples.app

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(examples.app.run())

def test_get_project_responses(client):
    """Test get_project_responses"""
    response = client.simulate_get('/page/get_project_responses')
    assert response.status_code == 200

    content = json.loads(response.content)

    assert content
    assert isinstance(content, list)

    response = content[0]
    # pylint: disable=line-too-long
    assert list(response.keys()) == ['id', 'sequential_id', 'project_id', 'form_id', 'initial_response_id', 'pretty_id', 'submitted_at', 'responses', 'rating_aggregates', 'average_rating', 'num_ratings', 'created_at', 'updated_at', 'status', 'labels', 'responder_language', 'responder', 'deleted_at', 'submission_source']

    assert isinstance(response['id'], int)

def test_get_project_labels(client):
    """Test get_project_labels"""
    response = client.simulate_get('/page/get_project_labels')
    assert response.status_code == 200

    content = json.loads(response.content)
    assert isinstance(content, list)

def test_update_project_response_labels_none(client):
    """Test update_project_response_labels_none"""
    labels = []
    response = client.simulate_get('/page/update_project_response_labels_none')
    content = json.loads(response.content)
    assert labels == content['labels']

def test_update_project_response_labels_all(client):
    """Test update_project_response_labels_all"""
    response = client.simulate_get('/page/get_project_labels')
    project_labels = json.loads(response.content)
    labels = []
    if project_labels:
        for label in project_labels:
            labels.append(label['name'])

    response = client.simulate_get('/page/update_project_response_labels_all')
    content = json.loads(response.content)
    assert labels == content['labels']
