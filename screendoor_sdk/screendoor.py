""" screendoor module """
import requests
class Screendoor(object):
    """ Screendoor class """
    def __init__(self, api_key, version='0', host='https://screendoor.dobt.co/api'):
        self.host = host
        self.api_key = api_key
        self.version = version

    def get_url(self, options):
        """ Produce API URL """
        url = self.host + options['path']
        url += '?v=' + self.version
        url += '&api_key=' + self.api_key
        if 'params' in options:
            for key, value in options['params'].items():
                url += '&' + str(key) + '=' + str(value)
        return url

    def get_project_responses(self, project_id, params=None, pages=1):
        """ Get Responses by Project """
        first_page = int(params.pop('page', 1)) if params else 1
        per_page = int(params.pop('per_page', 100)) if params else 100

        url = self.get_url({
            'path' : '/projects/' + str(project_id) + '/responses',
            'params' : params
        })

        responses = []
        for page in range(first_page, pages+first_page):
            response = requests.get(url, {'per_page': str(per_page), 'page' : str(page)})
            data = response.json()
            if data:
                responses += data
            else:
                break
        return responses

    def get_project_labels(self, project_id):
        """ Get labels by project """
        url = self.get_url({
            'path' : '/projects/' + str(project_id) + '/labels'
        })
        labels = []
        response = requests.get(url)
        if response.status_code == 200:
            labels = response.json()
        return labels

    def update_project_response(self, project_id,
                                response_id, response_fields=None,
                                status=None, labels=None, force_validation=False):
        """ Update project response """
        response = {}
        url = self.get_url({
            'path' : '/projects/' + str(project_id) + '/responses/' + str(response_id),
        })
        data = {}
        if response_fields is not None:
            data['response_fields'] = response_fields
        if status is not None:
            data['status'] = status
        if labels is not None:
            data['labels'] = labels
        if data:
            data['force_validation'] = force_validation
            response = requests.put(url, json=data)
        return response
