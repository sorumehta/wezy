class Request:
    def __init__(self, http_method, resource, headers=None, parameters=None, socket_of=None):
        self.http_method = http_method
        self.resource = resource
        self.headers = headers
        self.parameters = parameters
        self.socket_of = socket_of
