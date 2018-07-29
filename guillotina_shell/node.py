from os.path import join

from guillotina_client.swagger import EndpointProducer


class Node:
    def __init__(self, path, client):
        self.client = client
        self.path = path
        self.endpoints = {}
        instance = EndpointProducer(self.swagger)
        for endpoint in instance.endpoint_generator():
            self.endpoints[endpoint.endpoint] = endpoint

    @property
    def swagger(self):
        url_swagger = join(self.path, '@swagger')
        swagger_response = self.client.get_request(url_swagger)
        return swagger_response
