from util.helpers import assert_equals
from util.multipart import parse_multipart
from util.request import Request

def create_multipart_request(boundary, parts):
    boundary = boundary.encode()
    request_data = b"METHOD /path HTTP/1.1\r\n"
    request_data += b"Content-Type: multipart/form-data; boundary=" + boundary + b"\r\n"
    for element in parts:
        headers = element.get("headers")
        content = element.get("content")
        request_data += b"\r\n--" + boundary + b"\r\n"
        for key in headers.keys():
            request_data += key.encode() + b":" + headers.get(key).encode() + b"\r\n"
        request_data += b"\r\n" + content
    request_data += b"\r\n--" + boundary + b"--\r\n"
    request = Request(request_data)
    return parse_multipart(request)

def test(title, multipart_request, boundary, parts):
    print(title)
    assert_equals(boundary, multipart_request.boundary)
    for index in range(len(parts)):
        part1 = parts[index]
        part2 = multipart_request.parts[index]
        name = part1.get("name").strip("\"")
        headers = part1.get("headers")
        content = part1.get("content")
        assert_equals(name, part2.name)
        assert_equals(headers, part2.headers)
        assert_equals(content, part2.content)
    print(title + " passed\n")

def test1():
    title = "Test 1"
    boundary = "----WebKitFormBoundarycriD3u6M0UuPR1ia"
    parts = [
        {
            "name": "\"name\"",
            "headers": {
                "Content-Disposition": "form-data; name=\"name\"",
            },
            "content": b"content",
        },
    ]
    multipart_request = create_multipart_request(boundary, parts)
    test(title, multipart_request, boundary, parts)

def test2():
    title = "Test 2"
    boundary = ""
    parts = [
        {
            "name": "\"name\"",
            "headers": {
                "Content-Disposition": "form-data; name=\"name\"",
            },
            "content": b"content",
        },
    ]
    multipart_request = create_multipart_request(boundary, parts)
    test(title, multipart_request, boundary, parts)

def test3():
    title = "Test 3"
    boundary = "----WebKitFormBoundarycriD3u6M0UuPR1ia"
    parts = [
        {
            "name": "\"name\"",
            "headers": {
                "Content-Disposition": "form-data; name=\"name\"",
            },
            "content": b"",
        },
    ]
    multipart_request = create_multipart_request(boundary, parts)
    test(title, multipart_request, boundary, parts)

def test4():
    title = "Test 4"
    boundary = "----WebKitFormBoundarycriD3u6M0UuPR1ia"
    parts = [
        {
            "name": "\"name1\"",
            "headers": {
                "Content-Disposition": "form-data; name=\"name1\"; option: value",
                "Content-Type": "text/plain",
            },
            "content": b"content1",
        },
        {
            "name": "\"name2\"",
            "headers": {
                "Content-Disposition": "form-data; name=\"name2\"; option: value",
                "Content-Type": "text/plain",
            },
            "content": b"content2",
        },
    ]
    multipart_request = create_multipart_request(boundary, parts)
    test(title, multipart_request, boundary, parts)

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    print("util/multipart.py passed all tests\n")