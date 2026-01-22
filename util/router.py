from util.response import Response
import json

class Route:
    def __init__(self, method, path, action, exact_path=False):
        self.method = method
        self.path = path
        self.action = action
        self.exact_path = exact_path
    
    def matches(self, request):
        if request.method != self.method:
            return False
        if request.path == self.path:
            return True
        if request.path.startswith(self.path) and not self.exact_path:
            return True
        return False

class Router:
    def __init__(self):
        self.routes = []
        self.ws_routes = []
    
    def add_route(self, method, path, action, exact_path=False):
        self.routes.append(Route(method, path, action, exact_path))
    
    def add_ws_route(self, message_type, action):
        self.ws_routes.append(WSRoute(message_type, action))
    
    def route_request(self, request, handler):
        for element in self.routes:
            if element.matches(request):
                element.action(request, handler)
                return
        response = Response(404)
        response.send(handler)
    
    def route_ws_payload(self, payload, auth_token, handler):
        payload = json.loads(payload)
        message_type = payload.get("messageType")
        for element in self.ws_routes:
            if element.message_type == message_type:
                element.action(payload, auth_token, handler)
                return

class WSRoute:
    def __init__(self, message_type, action):
        self.message_type = message_type
        self.action = action