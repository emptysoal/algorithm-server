import time
import json
import base64
import uuid
import random
from multiprocessing import Process

import requests

tasks = [
    {"path": "./test_images/dog.jpg", "type": "detection"},
    {"path": "./test_images/roses_03.jpg", "type": "classification"},
    {"path": "./test_images/single.jpeg", "type": "detection"},
    {"path": "./test_images/sunflowers_04.jpeg", "type": "classification"},
]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encode_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encode_string


def request_inference(image_path, alg_type, ip, port):
    start = time.time()

    encode_string = encode_image(image_path)

    code = uuid.uuid4().int
    data = {
        "algorithm": alg_type,
        "image": encode_string,
        "code": code
    }

    response = requests.post("http://%s:%s/inference" % (ip, port), data=json.dumps(data))
    data = json.loads(response.text)
    if data["status"] != 200:
        print(data["msg"])
        return

    while True:
        response2 = requests.post("http://%s:%s/result" % (ip, port), data=json.dumps({"code": code}))
        data = json.loads(response2.text).get("data", {})
        if data:
            cost = time.time() - start
            print("%16s  %.2fs  %36s  %s" % (alg_type, cost, image_path, data))
            break

        if time.time() - start > 60:
            print("timeout...")
            break


def run(ip, port):
    p_list = []
    for i in range(20):
        idx = random.randint(0, 3)
        p = Process(target=request_inference, args=(tasks[idx]["path"], tasks[idx]["type"], ip, port))
        p.start()
        p_list.append(p)

    [p.join() for p in p_list]


if __name__ == '__main__':
    # request_inference("./test_images/single.jpeg", "detection", "192.168.0.230", 32802)
    run("192.168.0.230", 32802)
