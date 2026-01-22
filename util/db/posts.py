from pathlib import Path
from util.media import create_media, create_media_html, sniff_media_type
from util.db.accounts import retrieve_account, guest_username
from util.db.mongo import create_record, delete_record, list_records, retrieve_record, update_record, posts
import html
import json

def create_chat_post(message, auth_token, xsrf_token):
    message = html.escape(message)
    post = {"message": message}
    return create_post(post, auth_token, xsrf_token)

def create_media_post(media_data:bytes, auth_token, xsrf_token):
    if len(media_data) == 0:
        return None
    post = {"message": ""}
    post_id = create_post(post, auth_token, xsrf_token)
    if post_id is None:
        return None
    media_type = sniff_media_type(media_data)
    file_path = create_media(media_data, "./public/image/uploads/", media_type)
    if file_path is None:
        post["message"] = "media format not recognized"
        return post_id
    media_html = create_media_html(file_path, media_type, 240, 240)
    post["message"] = media_html
    post["file_path"] = file_path
    update_record(posts, {"id": post_id}, post)
    return post_id

def create_post(post, auth_token, xsrf_token):
    username = guest_username
    account = retrieve_account(auth_token)
    if account is not None:
        if xsrf_token is None:
            return None
        if xsrf_token != account.get("xsrf_token"):
            return None
        username = account.get("username")
    post["username"] = username
    return create_record(posts, post)

def delete_post(post_id, auth_token):
    username = guest_username
    account = retrieve_account(auth_token)
    if account is not None:
        username = account.get("username")
    post = retrieve_post(post_id)
    if post is not None:
        if username != post.get("username"):
            return False
        file_path = post.get("file_path")
        if file_path is not None:
            file = Path(file_path)
            file.unlink(True)
        delete_record(posts, {"id": post_id})
    return True

def list_posts():
    return list_records(posts)

def purge_posts():
    posts.delete_many({})

def purge_uploads():
    directory = Path("./public/image/uploads/")
    for element in directory.iterdir():
        element.unlink()

def retrieve_post(post_id):
    return retrieve_record(posts, {"id": post_id})

def ws_create_chat_post(message, auth_token, xsrf_token):
    username = guest_username
    account = retrieve_account(auth_token)
    if account is not None:
        username = account.get("username")
    message = html.escape(message)
    post = {"message": message}
    post_id = create_post(post, auth_token, xsrf_token)
    if post_id is None:
        return None
    payload = {
        "messageType": "chatMessage",
        "username": username,
        "message": message,
        "id": post_id
    }
    return payload