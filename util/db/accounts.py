from util.auth import validate_password
from util.db.mongo import create_record, retrieve_record, update_record, accounts
import bcrypt
import hashlib
import html
import uuid

def login_account(username, password):
    username = html.escape(username)
    account = retrieve_record(accounts, {"username": username})
    if account is None:
        return None
    account_id = account.get("id")
    salt = account.get("salt", bcrypt.gensalt())
    password_hash = bcrypt.hashpw(password.encode(), salt)
    if password_hash != account.get("password"):
        return None
    auth_token = str(uuid.uuid4())
    auth_token_hash = hashlib.sha256(auth_token.encode()).digest()
    update_record(accounts, {"id": account_id}, {"auth_token": auth_token_hash})
    return auth_token

def login_third_party_account(username):
    username = html.escape(username)
    account = retrieve_record(accounts, {"username": username})
    if account is None:
        return None
    account_id = account.get("id")
    auth_token = str(uuid.uuid4())
    auth_token_hash = hashlib.sha256(auth_token.encode()).digest()
    update_record(accounts, {"id": account_id}, {"auth_token": auth_token_hash})
    return auth_token

def logout_account(auth_token):
    account = retrieve_account(auth_token)
    if account is None:
        return False
    account_id = account.get("id")
    update_record(accounts, {"id": account_id}, {"auth_token": None})
    return True

def purge_accounts():
    accounts.delete_many({})

def register_account(username, password):
    username = html.escape(username)
    account = retrieve_record(accounts, {"username": username})
    if account is not None:
        return None
    if not validate_password(password):
        return None
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    account = {"username": username, "password": password_hash, "salt": salt}
    return create_record(accounts, account)

def register_third_party_account(username, access_token):
    username = html.escape(username)
    account = retrieve_record(accounts, {"username": username})
    if account is not None:
        return None
    account = {"username": username, "access_token": access_token}
    return create_record(accounts, account)

def retrieve_account(auth_token):
    if auth_token is None:
        return None
    auth_token_hash = hashlib.sha256(auth_token.encode()).digest()
    return retrieve_record(accounts, {"auth_token": auth_token_hash}) 

def update_xsrf_token(account):
    if account is None:
        return None
    account_id = account.get("id")
    xsrf_token = str(uuid.uuid4())
    update_record(accounts, {"id": account_id}, {"xsrf_token": xsrf_token})
    return xsrf_token

guest_username = "Guest"