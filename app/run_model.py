import torch
import numpy as np

from app.preprocess import get_face
from model.arch import resnest_cropped


async def model_evaluate(img):
    model = resnest_cropped()
    model.load_state_dict(torch.load("model/model_best.pkl", map_location=torch.device('cpu'))["state"])
    model.eval()

    face = await get_face(img)

    if face is None:
        return None

    with torch.no_grad():
        cls = torch.argmax(model(face))  # 0 for positive 1 for negative -> mapping to text
    return int(cls)
