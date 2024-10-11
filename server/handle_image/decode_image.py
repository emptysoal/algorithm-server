import base64
from PIL import Image
from io import BytesIO


def decode(encode_string, output_path="./res.jpg"):
    decode_string = base64.b64decode(encode_string)
    pil_image = Image.open(BytesIO(decode_string))
    # pil_image.save(output_path)
    return pil_image
