from queue import Queue
from threading import Thread

from handle_image.decode_image import decode
from handle_image.classification.infer import Classifier
from handle_image.detection.infer import Detector

from tools.make_logger import Logger

logger = Logger().get_logger(__name__)

# 创建各算法对应得队列，从这些队列中获取相应得任务
class_queue = Queue()
detect_queue = Queue()
# 创建算法结果输出队列，算法推理结果统一放入此队列
res_queue = Queue()


def classify(in_queue, out_queue, device=0):
    # 加载模型，构建推理实例
    classifier = Classifier("./handle_image/classification/model/best.pth", "cuda:%d" % device)
    logger.info("Classification model load successfully.")

    while True:
        task = in_queue.get()
        code = task["code"]
        encode_image = task["image"]
        logger.info("Succeed getting base64 encode image data.")

        # 图像数据解码
        pil_img = decode(encode_image)
        logger.info("Succeed to decode base64 image data.")

        # 模型推理
        res = classifier.infer(pil_img)
        res["code"] = code
        logger.info("Succeed getting inference result, which is %s." % res)

        out_queue.put(res)


def detect(in_queue, out_queue):
    # 加载模型，构建推理实例
    detector = Detector("./handle_image/detection/weights/yolov8s.pt")
    logger.info("Detection model load successfully.")

    while True:
        task = in_queue.get()
        code = task["code"]
        encode_image = task["image"]
        logger.info("Succeed getting base64 encode image data.")

        # 图像数据解码
        pil_img = decode(encode_image)
        logger.info("Succeed to decode base64 image data.")

        # 模型推理
        res = detector.infer(pil_img)
        res["code"] = code
        logger.info("Succeed getting inference result, which is %s." % res)

        out_queue.put(res)


def start_alg_process():
    """
        开启各算法子进程
    """
    for i in range(2):
        # p_c = Process(target=classify, args=(class_queue, res_queue, 0))
        p_c = Thread(target=classify, args=(class_queue, res_queue, i + 1))
        p_c.start()
    for _ in range(2):
        # p_d = Process(target=detect, args=(detect_queue, res_queue))
        p_d = Thread(target=detect, args=(detect_queue, res_queue))
        p_d.start()
