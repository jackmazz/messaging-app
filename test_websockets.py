from util.helpers import assert_equals
from util.websockets import parse_ws_frame
import random

def create_ws_frame(fin_bit, rsv_bits, opcode, payload:bytes, mask:bytes=None):
    mask_bit = 0 if mask is None else 1
    extended_payload_length = None
    payload_length = len(payload)
    payload_width = None
    if payload_length >= 126 and payload_length < 65536:
        extended_payload_length = payload_length
        payload_length = 126
        payload_width = 2
    elif payload_length >= 65536:
        extended_payload_length = payload_length
        payload_length = 127
        payload_width = 8
    frame_data = ((fin_bit << 15) + (rsv_bits << 12) + (opcode << 8) + (mask_bit << 7) + payload_length).to_bytes(2)
    if extended_payload_length is not None:
        frame_data += extended_payload_length.to_bytes(payload_width)
    if mask is None:
        mask = b"\x00\x00\x00\x00"
    else:
        frame_data += mask
    for index in range(len(payload)):
        frame_data += (payload[index] ^ mask[index % 4]).to_bytes(1)
    return parse_ws_frame(frame_data)

def test(title, ws_frame, fin_bit, rsv_bits, opcode, payload:bytes, mask:bytes=None):
    print(title)
    print("mask was: " + str(mask))
    assert_equals(fin_bit, ws_frame.fin_bit, "fin_bits")
    assert_equals(rsv_bits, ws_frame.rsv_bits, "rsv_bits")
    assert_equals(opcode, ws_frame.opcode, "opcode")
    assert_equals(len(payload), ws_frame.payload_length, "payload_length")
    assert_equals(payload, ws_frame.payload, "payload", False)
    print(title + " passed\n")

def test1():
    title = "Test 1"
    fin_bit = 0
    rsv_bits = 0
    opcode = 0
    payload = b""
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test2():
    title = "Test 2"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b""
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test3():
    title = "Test 3"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"hello world"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test4():
    title = "Test 4"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"hello world"
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test5():
    title = "Test 5"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 125
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test6():
    title = "Test 6"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 125
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test7():
    title = "Test 7"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 126
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test8():
    title = "Test 8"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 126
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test9():
    title = "Test 9"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 65535
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test10():
    title = "Test 10"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 65535
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test11():
    title = "Test 11"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 65536
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test12():
    title = "Test 12"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 65536
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test13():
    title = "Test 13"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 18446744073709551615
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload)

def test14():
    title = "Test 14"
    fin_bit = 1
    rsv_bits = 0
    opcode = 1
    payload = b"x" * 18446744073709551615
    mask = b"\xDE\xAD\xBE\xEF"
    ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
    test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test_random(test_count):
    for count in range(test_count):
        title = "Random Test " + str(count + 1)
        fin_bit = random.randint(0, 1)
        rsv_bits = random.randint(0, 7)
        opcode = random.randint(0, 15)
        payload = random.randbytes(random.randint(0, 100000))
        mask = random.randbytes(4)
        ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
        test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

def test_range(start, end):
    for count in range(start, end):
        title = "Range Test " + str(count - start + 1)
        fin_bit = random.randint(0, 1)
        rsv_bits = random.randint(0, 7)
        opcode = random.randint(0, 15)
        payload = random.randbytes(count)
        mask = random.randbytes(4)
        ws_frame = create_ws_frame(fin_bit, rsv_bits, opcode, payload, mask)
        test(title, ws_frame, fin_bit, rsv_bits, opcode, payload, mask)

if __name__ == "__main__":
    # test_random(100)
    # test_range(0, 65536)
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
    print("util/websockets.py passed all tests")