def assert_equals(expected, actual, title, print_enabled=True):
    if expected != actual:
        if print_enabled:
            print("Assertion failed for " + title + "; expected: " + repr(expected) + " != actual: " + repr(actual))
        else:
            print("Assertion failed for " + title)
        exit()
    if print_enabled:
        print("Assertion passed for " + title + "; expected: " + repr(expected) + " == actual: " + repr(actual))
    else:
        print("Assertion passed for " + title)

def create_url(path, query):
    url = path
    query_start = "?"
    separator = ""
    for key in query:
        url += query_start + separator + key + "=" + query[key]
        query_start = ""
        separator = "&"
    return url

def decode_url(string):
    index = 0
    while index < len(string):
        if index + 3 <= len(string):
            substring = string[index: index + 3]
            if substring[0] == "%":
                decoded = chr(int(substring[1:], 16))
                string = string[:index] + decoded + string[index + 3:]
        index += 1
    return string

def divide_byte_array(byte_array:bytes, separator:bytes, length = 0):
    split = byte_array.split(separator, length - 1)
    while len(split) < length:
        split.append(b"")
    return split

def divide_string(string, separator, length = 0):
    split = string.split(separator, length - 1)
    while len(split) < length:
        split.append("")
    return split

def extract_bits(byte, start, end):
    rshift = 8 - end
    mask = pow(2, end - start) - 1
    byte >>= rshift
    byte &= mask
    return int(byte)

def find_header_option(header, key):
    index = header.find(";")
    if index == -1:
        return ""
    substring = header[index + 1:]
    dictionary = parse_dictionary(substring, "=", ";")
    return dictionary.get(key, "")

def get_header_value(header):
    index = header.find(";")
    if index == -1:
        return ""
    substring = header[:index]
    return substring

def parse_dictionary(string, delimiter=":", separator=","):
    dictionary = {}
    for element in string.split(separator):
        split = element.split(delimiter, 1)
        if len(split) == 2:
            key = split[0].strip()
            value = split[1].strip()
            dictionary[key] = value
    return dictionary

def parse_url_query(url):
    index = url.find("?")
    if index == -1:
        return {}
    query_string = url[index + 1:]
    query = parse_dictionary(query_string, "=", "&")
    return query

def string_list_append(string, value, separator=","):
    if string != "":
        string += separator
    string += str(value)
    return string