from util.helpers import create_url, parse_url_query
import base64
import json
import os
import requests

def create_spotify_redirect_url():
    client_id = os.environ.get("CLIENT_ID")
    redirect_uri = os.environ.get("REDIRECT_URI")
    path = "https://accounts.spotify.com/authorize"
    scope = 'user-read-private user-read-email'
    query = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
    }
    return create_url(path, query)

def request_spotify_access_token(url):
    query = parse_url_query(url)
    code = query.get("code")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")
    path = "https://accounts.spotify.com/api/token"
    authorization = str(client_id) + ":" + str(client_secret)
    authorization = "Basic " + base64.b64encode(authorization.encode()).decode()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": authorization,
    }
    response = requests.post(path, data=data, headers=headers)
    content = json.loads(response.content)
    return content.get("access_token")

def request_spotify_user_email(access_token):
    if access_token is None:
        return None
    path = "https://api.spotify.com/v1/me"
    authorization = "Bearer " + access_token
    headers = {"Authorization": authorization}
    response = requests.get(path, headers=headers)
    content = json.loads(response.content)
    return content.get("email")