# -*- coding = utf-8 -*-

import json
import flask

from alg_process import class_queue, detect_queue, res_queue, start_alg_process
from tools.make_logger import Logger

logger = Logger().get_logger(__name__)

# 从输出队列中获取推理结果，并存储到下面得字典中
res_dict = {}  # {"code": fgd, "cls": "person", ...}

server = flask.Flask(__name__)


@server.route("/connect-test", methods=["get"])
def test_connect():
    return flask.jsonify({"status": 200, "msg": "success"})


@server.route("/inference", methods=["post"])
def alg_infer():
    params = json.loads(flask.request.get_data())
    algorithm = params["algorithm"]  # 获取算法类型（分类/检测）
    # 模型推理
    if algorithm == "classification":
        class_queue.put(params)
    elif algorithm == "detection":
        detect_queue.put(params)
    else:
        msg = "Do not support the given task."
        logger.error(msg)
        return flask.jsonify({"status": 500, "msg": msg})

    return flask.jsonify({"status": 200, "msg": "success"})


@server.route("/result", methods=["post"])
def get_infer_result():
    params = json.loads(flask.request.get_data())
    request_code = params["code"]

    # 先把所有推理结果从 res_queue 中拿出来，存放到 res_dict 中
    while not res_queue.empty():
        output = res_queue.get()
        code = output.pop("code")
        res_dict[code] = output

    # 如果请求的 code 在 res_dict 中存在，则返回该值
    if request_code in res_dict:
        output = res_dict.pop(request_code)
        return flask.jsonify({"status": 200, "msg": "success", "data": output})

    return flask.jsonify({"status": 200, "msg": "success", "data": {}})


if __name__ == '__main__':
    start_alg_process()
    server.run(port=32802, host="0.0.0.0")
