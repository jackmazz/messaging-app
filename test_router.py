from util.helpers import assert_equals
from util.request import Request
from util.router import Router

class PhonyHandler:
    def __init__(self):
        self.request = PhonySocket()

class PhonySocket:
    def sendall(self, request):
        pass

action_called = None

def action1(request, handler):
    global action_called
    action_called = action1

def action2(request, handler):
    global action_called
    action_called = action2

def action3(request, handler):
    global action_called
    action_called = action3

def action4(request, handler):
    global action_called
    action_called = action4

def action5(request, handler):
    global action_called
    action_called = action5

def test(title, routes, request, action):
    global action_called
    print(title)
    router = Router()
    for element in routes:
        router.add_route(element[0], element[1], element[2], element[3])
    router.route_request(Request(request), PhonyHandler())
    assert_equals(action, action_called)
    print(title + " passed\n")
    action_called = None

def test1():
    title = "Test 1"
    routes = []
    request = b""
    action = None
    test(title, routes, request, action)

def test2():
    title = "Test 2"
    routes = [
        ["GET", "/public/image/cat.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    action = None
    test(title, routes, request, action)

def test3():
    title = "Test 3"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, False],
        ["GET", "/public/image/cat.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test4():
    title = "Test 4"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, True],
        ["GET", "/public/image/cat.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test5():
    title = "Test 5"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, False],
        ["GET", "/public/image/cat.jpg", action2, True],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test6():
    title = "Test 6"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, True],
        ["GET", "/public/image/cat.jpg", action2, True],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test7():
    title = "Test 7"
    routes = [
        ["GET", "/public/image/", action1, False],
        ["GET", "/public/image/dog.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test8():
    title = "Test 8"
    routes = [
        ["GET", "/public/image/", action1, False],
        ["GET", "/public/image/dog.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action1)

def test9():
    title = "Test 9"
    routes = [
        ["GET", "/public/image/", action1, True],
        ["GET", "/public/image/dog.jpg", action2, False],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action2)

def test10():
    title = "Test 10"
    routes = [
        ["GET", "/public/image/", action1, True],
        ["GET", "/public/image/dog.jpg", action2, True],
    ]
    request = b"GET /public/image/dog.jpg HTTP/1.1"
    test(title, routes, request, action2)

def test11():
    title = "Test 11"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, False],
        ["GET", "/public/image/", action2, False],
    ]
    request = b"GET /public/image/ HTTP/1.1"
    test(title, routes, request, action2)

def test12():
    title = "Test 12"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, True],
        ["GET", "/public/image/", action2, False],
    ]
    request = b"GET /public/image/ HTTP/1.1"
    test(title, routes, request, action2)

def test13():
    title = "Test 13"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, False],
        ["GET", "/public/image/", action2, True],
    ]
    request = b"GET /public/image/ HTTP/1.1"
    test(title, routes, request, action2)

def test14():
    title = "Test 14"
    routes = [
        ["GET", "/public/image/dog.jpg", action1, True],
        ["GET", "/public/image/", action2, True],
    ]
    request = b"GET /public/image/ HTTP/1.1"
    test(title, routes, request, action2)

def test15():
    title = "Test 15"
    routes = [
        ["GET", "/chat-messages", action1, True],
        ["GET", "/", action2, True],
        ["GET", "/public/image/", action3, False],
        ["POST", "/chat-messages", action4, True],
        ["DELETE", "/chat-messages/", action5, False]
    ]
    request = b"DELETE /chat-messages/33245ab1-1e7a-4374-b1fe-bc977a5d5d54 HTTP/1.1"
    test(title, routes, request, action5)

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
    test14()
    test15()
    print("util/router.py passed all tests\n")