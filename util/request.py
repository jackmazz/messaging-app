from util.helpers import divide_byte_array, divide_string, parse_dictionary

class Request:
    def __init__(self, request_data:bytes):
        split1 = divide_byte_array(request_data, b"\r\n\r\n", 2)
        split2 = divide_string(split1[0].decode(), "\r\n", 2)
        split3 = divide_string(split2[0], " ", 3)
        self.method = split3[0]
        self.path = split3[1]
        self.http_version = split3[2]
        self.headers = parse_dictionary(split2[1], ":", "\r\n")
        cookie_header = self.headers.get("Cookie", "")
        self.cookies = parse_dictionary(cookie_header, "=", ";") 
        self.body = split1[1]
    
    def __str__(self):
        string = self.method + " " + self.path + " " + self.http_version + "\n"
        for key in self.headers:
            string += key + ": " + self.headers.get(key) + "\n"
        string += "--------------------BODY--------------------\n"
        if len(self.body) > 1000:
            string += str(self.body[0:500])
            string += "\n...\n"
            string += str(self.body[len(self.body) - 500:])
        else:
            string += str(self.body)
        return string