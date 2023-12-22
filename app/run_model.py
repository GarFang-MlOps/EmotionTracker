import cv2
import torch

from app.preprocess import get_face
from model.arch import resnest_cropped
from model.config import CLASS_MAPPING

# Example how get model prediction
# 0. install requirements and project egg (pip3 install -e .)
# 1. download model from s3
# 2. load model
model = resnest_cropped()
model.load_state_dict(torch.load("<model_path>")["state"])
model.eval()

# 3. read image
img = cv2.imread("/home/evgenii/repos/EmotionTracker/ok4.jpg")

# 4. preprocess image
face = get_face(img)
with torch.no_grad():
    cls = CLASS_MAPPING[torch.argmax(model(face))]  # 0 for positive 1 for negative -> mapping to text
    print(cls)
