from util.auth import extract_credentials, validate_password
from util.helpers import assert_equals
from util.request import Request

def test(title, username, password, url_username, url_password, valid):
    print(title)
    request = "POST /register HTTP/1.1\r\n"
    request += "\r\nusername=" + url_username + "&password=" + url_password
    credentials = extract_credentials(Request(request.encode()))
    assert_equals(2, len(credentials))
    assert_equals(username, credentials[0])
    assert_equals(password, credentials[1])
    assert_equals(valid, validate_password(credentials[1]))
    print(title + " passed\n")

def test1():
    title = "Test 1"
    username = ""
    password = ""
    url_username = ""
    url_password = ""
    test(title, username, password, url_username, url_password, False)

def test2():
    title = "Test 2"
    username = "abc123"
    password = "xyz456"
    url_username = "abc123"
    url_password = "xyz456"
    test(title, username, password, url_username, url_password, False)

def test3():
    title = "Test 3"
    username = "@"
    password = "="
    url_username = "%40"
    url_password = "%3D"
    test(title, username, password, url_username, url_password, False)

def test4():
    title = "Test 4"
    username = "abc!@#123"
    password = "#xyz$"
    url_username = "abc%21%40%23123"
    url_password = "%23xyz%24"
    test(title, username, password, url_username, url_password, False)

def test5():
    title = "Test 5"
    username = "abc123"
    password = "!@#$%^&()-_="
    url_username = "abc123"
    url_password = "%21%40%23%24%25%5E%26%28%29%2D%5F%3D"
    test(title, username, password, url_username, url_password, False)

def test6():
    title = "Test 6"
    username = "abc123"
    password = "%%%"
    url_username = "abc123"
    url_password = "%25%25%25"
    test(title, username, password, url_username, url_password, False)

def test7():
    title = "Test 7"
    username = "abc123"
    password = "aB1&"
    url_username = "abc123"
    url_password = "aB1%26"
    test(title, username, password, url_username, url_password, False)

def test8():
    title = "Test 8"
    username = "abc123"
    password = "aB1&____"
    url_username = "abc123"
    url_password = "aB1%26%5F%5F%5F%5F"
    test(title, username, password, url_username, url_password, True)

def test9():
    title = "Test 9"
    username = "abc123"
    password = "abcDEF123!@#"
    url_username = "abc123"
    url_password = "abcDEF123%21%40%23"
    test(title, username, password, url_username, url_password, True)

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
    print("util/auth.py passed all tests\n")