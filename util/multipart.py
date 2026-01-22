from util.helpers import divide_byte_array, find_header_option, get_header_value, parse_dictionary

class MultipartRequest:
    def __init__(self, request):
        self.method = request.method
        self.path = request.path
        self.http_version = request.http_version
        self.headers = request.headers
        self.cookies = request.cookies
        content_type_header = self.headers.get("Content-Type", "")
        self.boundary = find_header_option(content_type_header, "boundary")
        self.parts = parse_parts(request.body, self.boundary)
    
    def __str__(self):
        string = self.method + " " + self.path + " " + self.http_version + "s"
        for key in self.headers:
            string += "\n" + key + ": " + self.headers.get(key)
        for part in self.parts:
            string += "\n--------------------PART--------------------\n"
            string += str(part)
        return string

class Part:
    def __init__(self, part_data:bytes):
        split = divide_byte_array(part_data, b"\r\n\r\n", 2)
        self.headers = parse_dictionary(split[0].decode(), ":", "\r\n")
        content_disposition_header = self.headers.get("Content-Disposition", "")
        self.name = find_header_option(content_disposition_header, "name").strip("\"")
        self.content = split[1]

    def __str__(self):
        string = self.name + "\n"
        for key in self.headers:
            string += key + ": " + self.headers.get(key) + "\n"
        string += str(self.content)
        return string
 
def is_multipart(request):
    content_type = get_header_value(request.headers.get("Content-Type", ""))
    index = content_type.find("/")
    if index == -1:
        index = len(content_type)
    substring = content_type[:index]
    return substring == "multipart"

def find_multipart_content(request, name):
    for part in request.parts:
        if part.name == name:
            return part.content
    return None

def parse_multipart(request):
    return MultipartRequest(request)

def parse_parts(body:bytes, boundary):
    parts = []
    boundary = boundary.encode()
    start_boundary = b"--" + boundary + b"\r\n"
    middle_boundary = b"\r\n--" + boundary + b"\r\n"
    end_boundary = b"\r\n--" + boundary + b"--"
    split1 = divide_byte_array(body, end_boundary, 2)
    if split1[0].find(start_boundary) == -1:
        return []
    split2 = divide_byte_array(split1[0], start_boundary, 2)
    split3 = divide_byte_array(split2[1], middle_boundary)
    for element in split3:
        parts.append(Part(element))
    return parts