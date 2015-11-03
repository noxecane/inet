from . import message


class Router(object):

    def __init__(self):
        self.routes = {}

    def register(self, path, f):
        """Register a function for a specific route.

        It only allows one function of each route. So registering a route
        replaces the former handler.
        """
        self.routes[path] = f

    def route(self, req):
        """Choose the function to handle a :class:message.`_Message`.

        It returns None if none was found and false if the message
        doesn't expect routing.
        """
        if 'path' in req.meta:
            path = req.meta['path']
            if path in self.routes:
                return self.routes[path]
            else:
                return None
        else:
            return False

    @classmethod
    def transform(cls, url):
        """Extract the service and its path from a url.

        It actually creates a message in the process as it
        must be able to route such message
        """
        urllist = url.split('://')
        if len(urllist) != 2:
            raise ValueError('What kind of url is this')
        service = urllist[0]
        req = message.message(meta={'path': urllist[1]})
        return service, req
