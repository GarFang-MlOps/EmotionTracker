import pickle
import torch
from torch.utils.data import Dataset


class EmotionDataset(Dataset):
    def __init__(self, split_path: str):
        with open(split_path, 'rb') as f:
            data = pickle.load(f)
            self.images = data["images"]
            self.targets = data["targets"]
        assert len(self.images) == len(self.targets), "Broke Dataset"

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        return torch.tensor(self.images[idx]).permute(-1, 0, 1), torch.FloatTensor(self.targets[idx])
