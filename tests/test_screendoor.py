"""Tests for screendoorapi package"""
from screendoor_sdk.screendoor import Screendoor

def test_screendoor_url():
    """Test screen api url"""
    sd_key = 'SCREENDOOR_API_KEY'
    sd_project_id = '1234'
    params = {'per_page': 50, 'page' : 10}

    sd_api = Screendoor(sd_key, '0', 'https://screendoor.dobt.co/api')
    sd_url = sd_api.get_url({
        'path' : '/projects/' + sd_project_id + '/responses',
        'params' : params
    })

    expected_sd_url = 'https://screendoor.dobt.co/api/projects/'
    expected_sd_url += sd_project_id+'/responses?v=0&api_key='+sd_key+'&per_page=50&page=10'

    assert expected_sd_url == sd_url
