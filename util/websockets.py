from util.helpers import extract_bits
import base64
import hashlib

extra_data = b""
ws_connections = []

class WSFrame:
    def __init__(self, frame_data:bytes):
        mask = None
        payload_index = 2
        mask_bit = extract_bits(frame_data[1], 0, 1)
        self.fin_bit = extract_bits(frame_data[0], 0, 1)
        self.rsv_bits = extract_bits(frame_data[0], 1, 4)
        self.opcode = extract_bits(frame_data[0], 4, 8)
        self.payload_length = extract_bits(frame_data[1], 1, 8)
        self.header_length = 2
        if self.payload_length == 126:
            payload_index = 4
            self.header_length = 4
            self.payload_length = int.from_bytes(frame_data[2:payload_index])
        elif self.payload_length == 127:
            payload_index = 10
            self.header_length = 10
            self.payload_length = int.from_bytes(frame_data[2:payload_index])
        if mask_bit == 1:
            mask = frame_data[payload_index:payload_index + 4]
            payload_index += 4
            self.header_length += 4
        self.payload = frame_data[payload_index:payload_index + self.payload_length]
        if mask is None:
            return
        masked_payload = b""
        for index in range(len(self.payload)):
            masked_payload += (self.payload[index] ^ mask[index % 4]).to_bytes(1)
        self.payload = masked_payload
    
    def __str__(self):
        string = "fin: " + str(self.fin_bit) + "\n"
        string += "rsv: " + str(self.rsv_bits) + "\n"
        string += "opcode: " + str(self.opcode) + "\n"
        string += "header_length: " + str(self.header_length) + "\n"
        string += "payload_length: " + str(self.payload_length) + "\n"
        string += "payload_length_actual: " + str(len(self.payload)) + "\n"
        string += "--------------------PAYLOAD--------------------\n"
        if len(self.payload) > 1000:
            string += str(self.payload[0:500])
            string += "\n...\n"
            string += str(self.payload[len(self.payload) - 500:])
        else:
            string += str(self.payload)
        return string

def compute_accept(ws_key):
    guid = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    ws_accept = hashlib.sha1(ws_key.encode() + guid).digest()
    ws_accept = base64.b64encode(ws_accept).decode()
    return ws_accept

def generate_ws_frame(payload:bytes):
    frame_data = b"\x81"
    payload_length = len(payload)
    if payload_length < 126:
        frame_data += payload_length.to_bytes(1)
    elif payload_length >= 126 and payload_length < 65536:
        frame_data += b"\x7E"
        frame_data += payload_length.to_bytes(2)
    else:
        frame_data += b"\x7F"
        frame_data += payload_length.to_bytes(8)
    frame_data += payload
    return frame_data

def parse_ws_frame(frame_data:bytes):
    return WSFrame(frame_data)

def send_to_all(payload):
    ws_frame = generate_ws_frame(payload)
    for element in ws_connections:
        element.sendall(ws_frame)

def ws_init(handler, auth_token):
    ws_connections.append(handler.request)
    while True:
        payload = b""
        while True:
            ws_frame = recv_next_frame(handler)
            payload += ws_frame.payload
            if ws_frame.opcode == 8:
                ws_connections.remove(handler.request)
                return
            if ws_frame.fin_bit == 1:
                break
        handler.router.route_ws_payload(payload, auth_token, handler)

def recv_next_frame(handler):
    global extra_data
    max_buffer_size = 2048
    received_data = None
    if len(extra_data) == 0:
        received_data = handler.request.recv(max_buffer_size)
    else:
        received_data = extra_data
    ws_frame = parse_ws_frame(received_data)
    data_length = ws_frame.header_length + ws_frame.payload_length
    extra_data = received_data[data_length:]
    received_data = received_data[:data_length]
    received_data = handler.buffer(received_data, data_length, max_buffer_size)
    ws_frame = parse_ws_frame(received_data)
    print(str(ws_frame) + "\n")
    return ws_frame