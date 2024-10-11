import torch
from torchvision import transforms

from resnet50 import ResNet50


class Classifier:
    def __init__(self, model_path, device="cuda:0"):
        input_size = 224
        classes_num = 5
        self.index2class_name = {0: "daisy", 1: "dandelion", 2: "roses", 3: "sunflowers", 4: "tulips"}
        self.infer_transform = transforms.Compose([
            transforms.Resize(int(input_size * 1.143)),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.device = torch.device(device if torch.cuda.is_available() else "cpu")

        self.model = ResNet50(classes_num=classes_num)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.to(self.device)
        self.model.eval()

    def infer(self, pil_img):
        image_tensor = self.infer_transform(pil_img).unsqueeze(0)
        image_tensor = image_tensor.to(self.device)

        with torch.no_grad():
            out = self.model(image_tensor)
            # print(out)
            # 执行softmax
            ps = torch.exp(out)
            ps = ps / torch.sum(ps)

            score, cls = ps.topk(1, dim=1)
            # print(score)

        # return self.index2class_name[cls.item()], score.item()

        result = {
            "class": self.index2class_name[cls.item()],
            "score": round(score.item(), 2)
        }

        return result
