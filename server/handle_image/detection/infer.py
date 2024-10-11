import numpy as np
from ultralytics import YOLO
import cv2


class Detector:
    def __init__(self, model_path, device="cuda:0"):
        self.model = YOLO(model_path, task="detect")

        self.class_name_list = [
            "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
            "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
            "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
            "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
            "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
            "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
            "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
            "teddy bear", "hair drier", "toothbrush"
        ]

    def infer(self, pil_img):
        np_img = np.array(pil_img)
        np_img = np_img.astype(np.uint8)[:, :, ::-1]
        # cv2.imwrite("./res2.jpg", np_img)
        result = self.model(np_img)[0]

        output = {
            "bboxes": result.boxes.xyxy.tolist(),
            "classes": [self.class_name_list[int(item)] for item in result.boxes.cls.tolist()],
            "scores": [round(item, 2) for item in result.boxes.conf.tolist()],
        }

        return output
