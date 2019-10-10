# pylint: disable=line-too-long
"""Python module for interacting with the Screendoor API via the `requests <https://pypi.org/project/requests/>`_ module.

http://dobtco.github.io/screendoor-api-docs/
"""
import requests
class Screendoor(object):
    """
    | Declare Screendoor class

    :param api_key: API Key
    :type api_key: str
    :param version: API version
    :type version: str, optional
    :param host: API host URL
    :type host: str, optional
    """
    def __init__(self, api_key, version='1', host='https://screendoor.dobt.co/api'):
        self.host = host
        self.api_key = api_key
        self.version = version

    def get_url(self, options):
        """
        | Get API endpoint URL

        :param options: URL options
        :type options: dict
        :return: A URL string
        :rtype: str
        """
        url = self.host + options['path']
        url += '?v=' + self.version
        url += '&api_key=' + self.api_key
        if 'params' in options:
            for key, value in options['params'].items():
                url += '&' + str(key) + '=' + str(value)
        return url

    def get_project_responses(self, project_id, params=None, pages=1):
        """
        | List a project's responses

        :param project_id: Project ID
        :type project_id: str
        :param params: Query parameters
        :type params: dict, optional
        :return: A list of responses to a specified project
        :rtype: list
        """
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
        """
        | List a responses' labels (deprecated)
        | Note: Access to the response label API is only available in version 0.

        :param project_id: Project ID
        :type project_id: str
        :return: a list of labels belonging to a specified project
        :rtype: list
        """
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
        """
        | Updates the specified response.

        :param project_id: Project ID
        :type project_id: str
        :param response_id: Response ID
        :type response_id: str
        :param response_fields: Response fields. See http://dobtco.github.io/screendoor-api-docs/#spec-for-the-response-hash
        :type response_fields: dict
        :param status: Statutes set within the Screendoor project
        :type status: str
        :param labels: Label names already used in the project and new label names
        :type labels: list
        :param force_validation: Force validations errors if the response is invalid.
        :type force_validation: bool
        :return: Requests response
        :rtype: requests.Response()
        """
        response = None
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
