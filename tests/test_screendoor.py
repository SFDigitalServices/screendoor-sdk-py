"""Tests for screendoorapi package"""
import json
from unittest.mock import patch
from screendoor_sdk.screendoor import Screendoor

SD_KEY = 'SCREENDOOR_API_KEY'
SD_PROJECT_ID = '1234'

MOCK_RESPONSES = """[
    {
        "id": 11111,
        "sequential_id": 1,
        "project_id": 1,
        "form_id": 1,
        "initial_response_id": null,
        "pretty_id": "ABCDEFG",
        "submitted_at": "2019-01-02T00:00:00.000Z",
        "responses": {
            "hkf58ruh": {
                "checked": [
                    "Chocolate Chip"
                ]
            },
            "e88dqmqb": null
        },
        "rating_aggregates": {},
        "average_rating": null,
        "num_ratings": 0,
        "created_at": "2019-01-01T00:00:00.000Z",
        "updated_at": "2019-01-02T00:00:00.000Z",
        "status": "Triage",
        "labels": [],
        "responder_language": "en",
        "responder": {
            "name": "Test One",
            "email": "test.one@test.com"
        },
        "deleted_at": null,
        "submission_source": {
            "type": "frontend",
            "hostname": "forms.fm"
        }
    }
]"""



def test_get_url():
    """ Test get api url """
    params = {'per_page': 50, 'page' : 10}

    scrndr = Screendoor(SD_KEY, '0', 'https://screendoor.dobt.co/api')
    sd_url = scrndr.get_url({
        'path' : '/projects/' + SD_PROJECT_ID + '/responses',
        'params' : params
    })

    expected_sd_url = 'https://screendoor.dobt.co/api/projects/'
    expected_sd_url += SD_PROJECT_ID+'/responses?v=0&api_key='+SD_KEY+'&per_page=50&page=10'

    assert expected_sd_url == sd_url

def test_project_labels():
    """ Test project_labels """
    labels = [
        {"name": "Missing information", "color": "3600ff", "responses_count": 1},
        {"name": "Questionable", "color": "336699", "responses_count": 0}]

    scrndr = Screendoor(SD_KEY)
    with patch('screendoor_sdk.screendoor.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = labels
        responses = scrndr.get_project_labels(SD_PROJECT_ID)
    assert labels == responses

    with patch('screendoor_sdk.screendoor.requests.get') as mock_get:
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {'error': 'not authorized'}
        responses = scrndr.get_project_labels(SD_PROJECT_ID)
    assert [] == responses

def test_get_project_responses():
    """ Test get_project_responses """
    scrndr = Screendoor(SD_KEY)
    with patch('screendoor_sdk.screendoor.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(MOCK_RESPONSES)
        responses = scrndr.get_project_responses(SD_PROJECT_ID, {'page': 1}, 2)
    assert json.loads(MOCK_RESPONSES) + json.loads(MOCK_RESPONSES) == responses

    with patch('screendoor_sdk.screendoor.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        responses = scrndr.get_project_responses(SD_PROJECT_ID, {'page': 1}, 1)
    assert [] == responses

def test_update_project_response():
    """ TEST update_project_response """
    scrndr = Screendoor(SD_KEY)
    with patch('screendoor_sdk.screendoor.requests.put') as mock_put:
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = json.loads(MOCK_RESPONSES)
        responses = scrndr.update_project_response(
            SD_PROJECT_ID, 1, {"hkf58ruh": {"checked": ["Option 3"]}},
            'Submitted', ['Label One'])
    assert json.loads(MOCK_RESPONSES) == responses.json()

    with patch('screendoor_sdk.screendoor.requests.put') as mock_put:
        mock_json = """{"ok": false, "errors": {"responses_hkf58ruh": ["can't be blank"]}}"""
        mock_put.return_value.status_code = 400
        mock_put.return_value.json.return_value = json.loads(mock_json)
        responses = scrndr.update_project_response(
            SD_PROJECT_ID, 1, {"hkf58ruh": {"checked": ["Option 3"]}},
            'Submitted', ['Label One'], True)
    assert json.loads(mock_json) == responses.json()
