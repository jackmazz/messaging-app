from util.auth import extract_credentials
from util.media import retrieve_media, sniff_media_type
from util.multipart import is_multipart, find_multipart_content, parse_multipart
from util.request import Request
from util.response import Response
from util.router import Router
from util.spotify import create_spotify_redirect_url, request_spotify_access_token, request_spotify_user_email
from util.templates import create_home_page_html
from util.websockets import compute_accept, send_to_all, ws_init
from util.db.accounts import login_account, login_third_party_account, logout_account
from util.db.accounts import register_account, register_third_party_account, purge_accounts
from util.db.posts import create_chat_post, create_media_post, delete_post, list_posts, purge_posts
from util.db.posts import purge_uploads, ws_create_chat_post
import json
import os
import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/chat-messages", chat_list, True)
        self.router.add_route("GET", "/public/favicon.ico", get_favicon, True)
        self.router.add_route("GET", "/public/functions.js", get_functions, True)
        self.router.add_route("GET", "/public/home_page.html", get_home_page, True)
        self.router.add_route("GET", "/public/style.css", get_style, True)
        self.router.add_route("GET", "/public/webrtc.js", get_webrtc, True)
        self.router.add_route("GET", "/purge", purge, True)
        self.router.add_route("GET", "/websocket", ws_handshake, True)
        self.router.add_route("GET", "/", get_home_page, True)
        self.router.add_route("GET", "/public/image/uploads/", media_upload_retrieve, False)
        self.router.add_route("GET", "/public/image/", media_retrieve, False)
        self.router.add_route("GET", "/spotify-login", spotify_redirect, False)
        self.router.add_route("GET", "/spotify", spotify_login, False)
        self.router.add_route("POST", "/chat-messages", chat_create, True)
        self.router.add_route("POST", "/login", account_login, True)
        self.router.add_route("POST", "/logout", account_logout, True)
        self.router.add_route("POST", "/media-uploads", media_create, True)
        self.router.add_route("POST", "/register", account_register, True)
        self.router.add_route("DELETE", "/chat-messages/", chat_delete, False)
        self.router.add_ws_route("chatMessage", ws_chat_create)
        self.router.add_ws_route("webRTC-offer", None)
        self.router.add_ws_route("webRTC-answer", None)
        self.router.add_ws_route("webRTC-candidate", None)
        super().__init__(request, client_address, server)
    
    def buffer(self, received_data, data_length, max_buffer_size=2048):
        percent_complete = 0
        while len(received_data) < data_length:
            percent_complete_new = int((len(received_data) / data_length) * 100)
            if percent_complete != percent_complete_new:
                percent_complete = percent_complete_new
                print(str(percent_complete) + "% complete")
            bytes_remaining = data_length - len(received_data)
            buffer_size = min(max_buffer_size, bytes_remaining)
            received_data += self.request.recv(buffer_size)
        return received_data

    def handle(self):
        max_buffer_size = 2048
        received_data = self.request.recv(max_buffer_size)
        request = Request(received_data)
        content_length = int(request.headers.get("Content-Length", "0"))
        data_length = len(received_data) - len(request.body) + content_length
        received_data = self.buffer(received_data, data_length, max_buffer_size)
        request = Request(received_data)
        if is_multipart(request):
            request = parse_multipart(request)
        self.router.route_request(request, self)
        print(str(request) + "\n")

def account_register(request, handler):
    credentials = extract_credentials(request)
    register_account(credentials[0], credentials[1])
    response = Response(302)
    response.set_header("Location", "/")
    response.send(handler)

def account_login(request, handler):
    credentials = extract_credentials(request)
    auth_token = login_account(credentials[0], credentials[1])
    response = Response(302)
    response.set_header("Location", "/")
    if auth_token is not None:
        response.set_cookie("auth_token", auth_token, path="/", max_age=3600, secure=True)
    response.send(handler)

def account_logout(request, handler):
    auth_token = request.cookies.get("auth_token")
    logout_account(auth_token)
    response = Response(302)
    response.set_header("Location", "/")
    response.send(handler)

def chat_create(request, handler):
    body = json.loads(request.body)
    message = body.get("message", "")
    auth_token = request.cookies.get("auth_token")
    xsrf_token = body.get("xsrf_token")
    post_id = create_chat_post(message, auth_token, xsrf_token)
    if post_id is None:
        response = Response(403)
        response.send(handler)
        return
    post_ids = request.cookies.get("post_ids", "[]")
    post_ids_json = json.loads(post_ids)
    post_ids_json.append(post_id)
    post_ids = json.dumps(post_ids_json)
    response = Response(204)
    response.set_cookie("post_ids", post_ids, path="/", max_age=3600, http_only=False)
    response.send(handler)

def chat_delete(request, handler):
    post_id = request.path[request.path.rfind("/") + 1:]
    post_ids = request.cookies.get("post_ids", "[]")
    post_ids_json = json.loads(post_ids)
    if post_id in post_ids_json:
        post_ids_json.remove(post_id)
    post_ids = json.dumps(post_ids_json)
    auth_token = request.cookies.get("auth_token")
    authorized = delete_post(post_id, auth_token)
    if authorized == False:
        response = Response(403)
        response.send(handler)
        return
    response = Response(204)
    response.set_cookie("post_ids", post_ids, path="/", max_age=3600, http_only=False)
    response.send(handler)

def chat_list(request, handler):
    body = json.dumps(list_posts()).encode()
    response = Response(200)
    response.set_body(body, "json")
    response.send(handler)

def get_home_page(request, handler):
    auth_token = request.cookies.get("auth_token")
    visits = int(request.cookies.get("visits", 0)) + 1
    body = create_home_page_html(auth_token, visits).encode()
    response = Response(200)
    response.set_cookie("visits", visits, path="/", max_age=3600)
    response.set_body(body, "html")
    response.send(handler)

def get_favicon(request, handler):
    response = Response(200)
    response.read_body("./public/favicon.ico", "icon")
    response.send(handler)

def get_functions(request, handler):
    response = Response(200)
    response.read_body("./public/functions.js", "js")
    response.send(handler)

def get_style(request, handler):
    response = Response(200)
    response.read_body("./public/style.css", "css")
    response.send(handler)

def get_webrtc(request, handler):
    response = Response(200)
    response.read_body("./public/webrtc.js", "js")
    response.send(handler)

def media_create(request, handler):
    auth_token = request.cookies.get("auth_token")
    xsrf_token = find_multipart_content(request, "xsrf_token").decode()
    media_data = find_multipart_content(request, "upload")
    if media_data is None or xsrf_token is None:
        response = Response(400)
        response.send(response)
        return
    if len(media_data) == 0:
        response = Response(204)
        response.send(handler)
        return
    post_id = create_media_post(media_data, auth_token, xsrf_token)
    if post_id is None:
        response = Response(403)
        response.send(handler)
        return
    post_ids = request.cookies.get("post_ids", "[]")
    post_ids_json = json.loads(post_ids)
    post_ids_json.append(post_id)
    post_ids = json.dumps(post_ids_json)
    response = Response(302)
    response.set_header("Location", "/")
    response.set_cookie("post_ids", post_ids, path="/", max_age=3600, http_only=False)
    response.send(handler)

def media_retrieve(request, handler):
    media_data = retrieve_media("." + request.path, "./public/image/")
    if media_data == None:
        response = Response(404)
        response.send(handler)
        return
    media_type = sniff_media_type(media_data)
    if media_data == None:
        response = Response(400)
        response.send(handler)
        return
    response = Response(200)
    response.set_body(media_data, media_type)
    response.send(handler)

def media_upload_retrieve(request, handler):
    media_data = retrieve_media("." + request.path, "./public/image/uploads/")
    if media_data == None:
        response = Response(404)
        response.send(handler)
        return
    media_type = sniff_media_type(media_data)
    if media_data == None:
        response = Response(400)
        response.send(handler)
        return
    response = Response(200)
    response.set_body(media_data, media_type)
    response.send(handler)

def purge(request, handler):
    dev_mode = os.environ.get("DEV_MODE")
    if dev_mode != "enabled":
        response = Response(404)
        response.send(handler)
        return
    purge_accounts()
    purge_posts()
    purge_uploads()
    response = Response(302)
    response.set_header("Location", "/")
    if "post_ids" in request.cookies:
        response.set_cookie("post_ids", "[]", path="/", max_age=3600, http_only=False)
    response.send(handler)

def spotify_login(request, handler):
    access_token = request_spotify_access_token(request.path)
    if access_token is None:
        response = Response(403)
        response.send(handler)
        return
    email = request_spotify_user_email(access_token)
    if email is None:
        response = Response(403)
        response.send(handler)
        return
    register_third_party_account(email, access_token)
    auth_token = login_third_party_account(email)
    response = Response(302)
    response.set_header("Location", "/")
    if auth_token is not None:
        response.set_cookie("auth_token", auth_token, path="/", max_age=3600)
    response.send(handler)

def spotify_redirect(request, handler):
    url = create_spotify_redirect_url()
    response = Response(302)
    response.set_header("Location", url)
    response.send(handler)

def ws_chat_create(payload, auth_token, handler):
    message = payload.get("message")
    xsrf_token = payload.get("xsrf_token")
    payload = ws_create_chat_post(message, auth_token, xsrf_token)
    payload = json.dumps(payload).encode()
    send_to_all(payload)

def ws_handshake(request, handler):
    auth_token = request.cookies.get("auth_token")
    ws_key = request.headers.get("Sec-WebSocket-Key")
    ws_accept = compute_accept(ws_key)
    response = Response(101)
    response.set_header("Connection", "Upgrade")
    response.set_header("Upgrade", "websocket")
    response.set_header("Sec-WebSocket-Accept", ws_accept)
    response.send(handler)
    ws_init(handler, auth_token)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    print("Listening on port " + str(port))
    server.serve_forever()