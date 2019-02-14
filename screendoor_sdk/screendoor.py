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
        if options['params']:
            for key, value in options['params'].items():
                url += '&' + str(key) + '=' + str(value)
        return url

    def get_project_responses(self, project_id, params=None, pages=1):
        """ Get Responses by Project """
        first_page = int(params.pop('page', 1)) if params else 1
        per_page = int(params.pop('per_page', 100)) if params else 100

        url = self.get_url({
            'path' : '/projects/' + project_id + '/responses',
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
