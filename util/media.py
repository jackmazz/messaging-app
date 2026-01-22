from pathlib import Path
from util.response import mime_types
import uuid

file_signatures = {
    b"\x47\x49\x46\x38": [0, "gif"],
    b"\xff\xd8\xff": [0, "jpg"],
    b"\x66\x74\x79\x70": [4, "mp4"],
    b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a": [0, "png"],
}

image_types = {
    "jpg",
    "gif",
    "png",
}

video_types = {
    "mp4",
}

def create_media(media_data:bytes, directory_path, media_type):
    if media_type is None:
        return None
    media_id = str(uuid.uuid4())
    file_path = directory_path + media_id + "." + media_type
    file = open(file_path, "wb")
    file.write(media_data)
    file.close()
    return file_path

def create_media_html(file_path, media_type, width, height):
    if media_type is None:
        return None
    if media_type in image_types:
        mime_type = mime_types.get(media_type)
        html = "<img type=" + mime_type + " src=\"" + file_path + "\" alt=\"image not found\""
        html += "width=\"" + str(width) + "px\" height=\"" + str(height) + "px\"/>"
        # html = "<img type=" + mime_type + " src=\"" + file_path + "\" alt=\"image not found\"/>"
        return html
    if media_type in video_types:
        mime_type = mime_types.get(media_type)
        html =  "<video controls width=\"" + str(width) + "px\" height=\"" + str(height) + "px\">"
        html += "<source type=" + mime_type + " src=\"" + file_path + "\" alt=\"video not found\">"
        html += "</video>"
        # html =  "<video controls>"
        # html += "<source type=" + mime_type + " src=\"" + file_path + "\" alt=\"video not found\">"
        # html += "</video>"
        return html
    return None

def retrieve_media(file_path, directory_path):
    if not Path(file_path).is_file():
        return None
    file_name = file_path[len(directory_path):]
    if "/" in file_name:
        print("DEBUG:" + file_name)
        return None
    file = open(file_path, "rb")
    media_data = file.read()
    return media_data

def sniff_media_type(file_data):
    for key in file_signatures:
        value = file_signatures.get(key)
        offset = value[0]
        subarray = file_data[offset:offset + len(key)]
        if subarray == key:
            return value[1]
    return None