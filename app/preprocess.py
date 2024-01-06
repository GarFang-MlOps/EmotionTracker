import cv2
import torch
import numpy as np
from matplotlib import pyplot as plt


async def get_face(img: np.array):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)
    if len(faces_rect) == 0:
        return None
    else:
        x, y, w, h = sorted(faces_rect, reverse=False, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        img = cv2.resize(gray_img[y:y + h, x:x + w], (48, 48), interpolation=cv2.INTER_LANCZOS4)

        return torch.FloatTensor(img / 255).unsqueeze(0).unsqueeze(0)
