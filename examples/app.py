""" get_project_responses example """
import json
import os
import falcon
import jsend
from screendoor_sdk.screendoor import Screendoor

def run():
    """ run function"""
    api = falcon.API()
    api.add_route('/page/{name}', Page())
    api.add_sink(Page().default_error, '')
    return api

class Page():
    """ Page class """
    scrndr = None
    project_id = None
    response_id = None

    def on_get(self, _req, _resp, name):
        """ on page GET requests """
        dispatch = None
        if hasattr(self.__class__, name) and callable(getattr(self.__class__, name)):
            dispatch = getattr(self, name)
        if dispatch:
            self.scrndr = Screendoor(os.environ['SD_KEY'])
            self.project_id = os.environ['SD_PROJECT_ID']
            self.response_id = os.environ['SD_RESPONSE_ID']
        else:
            dispatch = self.default_page
        dispatch(_req, _resp)

    def default_page(self, _req, _resp):
        """ default page response """
        msg = {'message': 'hello'}
        _resp.body = json.dumps(jsend.success(msg))
        _resp.status = falcon.HTTP_200

    def default_error(self, _req, resp):
        """Handle default error"""
        resp.status = falcon.HTTP_404
        msg_error = jsend.error('404 - Not Found')
        resp.body = json.dumps(msg_error)

    def get_project_responses(self, _req, resp):
        """ screendoor project response """
        responses = self.scrndr.get_project_responses(
            self.project_id,
            {'per_page': 1, 'page' : 1},
            1
            )
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(responses)

    def get_project_labels(self, _req, resp):
        """ screendoor project labels """
        responses = self.scrndr.get_project_labels(self.project_id)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(responses)

    def update_project_response(self, _req, resp):
        """ update a project response """
        response_id = self.response_id
        response_fields = {}
        status = None
        labels = None
        force_validation = True
        response = self.scrndr.update_project_response(
            self.project_id, response_id, response_fields,
            status, labels, force_validation)
        if response:
            resp.status = str(response.status_code)
            resp.body = json.dumps(response.json())
        else:
            self.default_error(_req, resp)
