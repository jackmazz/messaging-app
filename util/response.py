class Response:
    def __init__(self, status_code):
        self.status_code = str(status_code)
        self.status_message = status_messages.get(status_code, "")
        self.headers = {}
        self.cookies = {}
        self.set_body(default_bodies.get(status_code, b""), "txt")
        for key in default_headers:
            self.set_header(key, default_headers[key])
    
    def read_body(self, file_path, file_type):
        file = open(file_path, "rb")
        file_data = file.read()
        self.set_body(file_data, file_type)
    
    def send(self, handler):
        response = "HTTP/1.1 " + self.status_code + " " + self.status_message + "\r\n"
        for key in self.headers:
            response += key + ": " + self.headers[key] + "\r\n"
        for key in self.cookies:
            response += "Set-Cookie: " + key + "=" + self.cookies[key] + "\r\n"
        response = (response + "\r\n").encode() + self.body
        handler.request.sendall(response)
    
    def set_body(self, body:bytes, file_type):
        mime_type = mime_types.get(file_type)
        self.body = body
        self.set_header("Content-Length", len(body))
        self.set_header("Content-Type", mime_type)
    
    def set_cookie(self, key, value, path=None, max_age=None, http_only=True, secure=False):
        options = []
        if path is not None:
            options.append("Path=" + path)
        if max_age is not None:
            options.append("Max-Age=" + str(max_age))
        if http_only:
            options.append("HttpOnly")
        if secure:
            options.append("Secure")
        value = str(value)
        for element in options:
            value += "; " + element
        self.cookies[key] = value
    
    def set_header(self, key, value):
        self.headers[key] = str(value)

default_bodies = {
    400: b"The request couldn't be recognized.",
    403: b"The request has been denied.",
    404: b"The requested content does not exist.",
}

default_headers = {
    "X-Content-Type-Options": "nosniff",
}

mime_types = {
    "css": "text/css; charset=utf-8",
    "html": "text/html; charset=utf-8",
    "icon": "text/x-icon",
    "gif": "image/gif",
    "js": "text/javascript; charset=utf-8",
    "jpg": "image/jpeg",
    "json": "application/json; charset=utf-8",
    "mp4": "video/mp4",
    "png": "image/png",
    "txt": "text/plain; charset=utf-8",
}

status_messages = {
    101: "Switching Protocols",
    200: "OK",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
}