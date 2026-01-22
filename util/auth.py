from util.helpers import decode_url, parse_dictionary

def extract_credentials(request):
    query = parse_dictionary(request.body.decode(), "=", "&")
    username = decode_url(query.get("username", ""))
    password = decode_url(query.get("password", ""))
    return [username, password]

def validate_password(password):
    if len(password) < 8:
        return False
    special_characters = "!@#$%^&()-_="
    validations = [False, False, False, False]
    for character in password:
        if character.islower():
            validations[0] = True
        elif character.isupper():
            validations[1] = True
        elif character.isnumeric():
            validations[2] = True
        elif character in special_characters:
            validations[3] = True
        else:
            return False
    return all(validations)