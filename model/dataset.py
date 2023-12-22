import pickle
import torch
from torch.utils.data import Dataset
import torchvision.transforms as T


class EmotionDataset(Dataset):
    def __init__(self, split_path: str):
        with open(split_path, 'rb') as f:
            data = pickle.load(f)
            self.images = data["images"]
            self.targets = data["targets"]
            self.targets_sampler = torch.argmax(torch.tensor(self.targets), dim=1)

        self.preprocess = T.Compose(
            [
                T.RandomHorizontalFlip(p=0.5),
                T.RandomRotation((-20, 20)),
            ]
        )
        assert len(self.images) == len(self.targets), "Broke Dataset"

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):

        img = torch.tensor(self.images[idx]).permute(-1, 0, 1) * 255
        img = self.preprocess(img)
        target_base = self.targets[idx]
        negative_emotions = [0, 1, 2, 4]
        target = [1, 0]
        # convert to positive / negative emotion
        for negative_emotion in negative_emotions:
            if target_base[negative_emotion] > 0:
                target = [0, 1]
                break

        return img, torch.FloatTensor(target)
