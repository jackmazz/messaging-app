from util.helpers import assert_equals
from util.request import Request

def create_request(method, path, http_version, headers, body:bytes):
    request_data = (method + " " + path + " " + http_version + "\r\n").encode()
    for element in headers.keys():
        request_data += (element + ": " + headers[element] + "\r\n").encode()
    request_data += b"\r\n" + body
    return Request(request_data)

def test(title, request, method, path, http_version, headers, cookies, body:bytes):
    print(title)
    assert_equals(method, request.method)
    assert_equals(path, request.path)
    assert_equals(http_version, request.http_version)
    assert_equals(headers, request.headers)
    assert_equals(cookies, request.cookies)
    assert_equals(body, request.body)
    print(title + " passed\n")

def test1():
    title = "Test 1"
    method = ""
    path = ""
    http_version = ""
    headers = {}
    cookies = {}
    body = b""
    request = Request(b"")
    test(title, request, method, path, http_version, headers, cookies, body)

def test2():
    title = "Test 2"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "localhost:8080", "Connection": "keep-alive"}
    cookies = {}
    body = b""
    request = create_request(method, path, http_version, headers, body)
    test(title, request, method, path, http_version, headers, cookies, body)

def test2():
    title = "Test 2"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "localhost:8080", "Connection": "keep-alive", "Cookie": "visits=4; cookie=value;"}
    cookies = {"visits": "4", "cookie": "value"}
    body = b""
    request = create_request(method, path, http_version, headers, body)
    test(title, request, method, path, http_version, headers, cookies, body)

def test3():
    title = "Test 3"
    method = "POST"
    path = "/path"
    http_version = "HTTP/1.1"
    headers = {"Content-Type": "text/plain", "Content-Length": "5"}
    cookies = {}
    body = b"hello"
    request = create_request(method, path, http_version, headers, body)
    test(title, request, method, path, http_version, headers, cookies, body)

def test4():
    title = "Test 4"
    method = "POST"
    path = "/path"
    http_version = "HTTP/1.1"
    headers = {"Content-Type": "text/plain", "Content-Length": "11", "Cookie": "visits=10; cookie=value;"}
    cookies = {"visits": "10", "cookie": "value"}
    body = b"hello world"
    request = create_request(method, path, http_version, headers, body)
    test(title, request, method, path, http_version, headers, cookies, body)

def test5():
    title = "Test 5"
    method = "POST"
    path = "/path"
    http_version = "HTTP/1.1"
    headers = {"Content  -  Type": "text  /  plain", "Content  -  Length": "17", "Cookie": "visits  =  13;   cookie  =  value;"}
    cookies = {"visits": "13", "cookie": "value"}
    body = b"  hello  world!  "
    string = "POST /path HTTP/1.1\r\n"
    string += "  Content  -  Type:   text  /  plain  \r\n"
    string += "  Content  -  Length:   17  \r\n"
    string += "  Cookie:   visits  =  13;   cookie  =  value;  \r\n\r\n"
    string += "  hello  world!  "
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test6():
    title = "Test 6"
    method = "POST"
    path = "/path"
    http_version = "HTTP/1.1"
    headers = {"Content-Type": "text/plain", "Content-Length": "13"}
    cookies = {}
    body = b"\r\nhello world"
    request = create_request(method, path, http_version, headers, body)
    test(title, request, method, path, http_version, headers, cookies, body)

def test7():
    title = "Test 7"
    method = "Content-Type:"
    path = "text/plain"
    http_version = ""
    headers = {"Content-Length": "11"}
    cookies = {}
    body = b"hello world"
    string = "Content-Type: text/plain\r\n"
    string += "Content-Length: 11\r\n\r\n"
    string += "hello world"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test8():
    title = "Test 8"
    method = "POST"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {}
    cookies = {}
    body = b"hello world"
    string = "POST / HTTP/1.1\r\n\r\n"
    string += "hello world"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test9():
    title = "Test 9"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "Connection:"}
    cookies = {}
    body = b""
    string = "GET / HTTP/1.1\r\n"
    string += "Host: Connection: \r\n\r\n"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test10():
    title = "Test 10"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "localhost:8080", "Connection": ""}
    cookies = {}
    body = b""
    string = "GET / HTTP/1.1\r\n"
    string += "Host: localhost:8080\r\n"
    string += "Connection: "
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test11():
    title = "Test 11"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "localhost:8080", "Connection": "keep-alive"}
    cookies = {}
    body = b""
    string = "GET / HTTP/1.1\r\n"
    string += "Host: localhost:8080\r\n"
    string += "Connection: keep-alive"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test12():
    title = "Test 12"
    method = "GET"
    path = "/"
    http_version = "HTTP/1.1"
    headers = {"Host": "localhost:8080", "Connection": "keep-alive"}
    cookies = {}
    body = b""
    string = "GET / HTTP/1.1\r\n"
    string += "Host: localhost:8080\r\n"
    string += "Connection: keep-alive\r\n\r\n"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

def test13():
    title = "Test 13"
    method = "POST"
    path = "/path"
    http_version = "HTTP/1.1"
    headers = {"Content-Type": "text/plain", "Content-Length": "29"}
    cookies = {}
    body = b"\r\nhello\r\n\r\nhello\r\n\r\nworld\r\n\r\n"
    string = "POST /path HTTP/1.1\r\n"
    string += "Content-Type: text/plain\r\n"
    string += "Content-Length: 29\r\n\r\n"
    string += "\r\nhello\r\n\r\nhello\r\n\r\nworld\r\n\r\n"
    request = Request(string.encode())
    test(title, request, method, path, http_version, headers, cookies, body)

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    test12()
    test13()
    print("util/request.py passed all tests\n")