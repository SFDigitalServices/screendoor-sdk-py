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
    def on_get(self, _req, _resp, name):
        """ on page GET requests """
        pages = {
            'get_project_responses' : self.get_project_responses
        }
        dispatch = pages.get(name, self.default_page)
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

    def get_project_responses(self, _req, _resp):
        """ screendoor page response """
        scrndr = Screendoor(os.environ['SD_KEY'])
        responses = scrndr.get_project_responses(
            os.environ['SD_PROJECT'],
            {'per_page': 1, 'page' : 1},
            1
            )
        _resp.status = falcon.HTTP_200
        _resp.body = json.dumps(responses)
