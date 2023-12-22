import argparse
import os.path
import random

import numpy as np
import torch

from model.dataset import EmotionDataset
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss
from torch.optim import RAdam
import wandb

from model.arch import resnest_cropped
from model.schedular import ReduceLR
from model.train_loop import train

parser = argparse.ArgumentParser(prog='Training CLF model')

parser.add_argument("--data_dir", type=str, default="data/", help="Path to train/test pkls")
parser.add_argument("--batch_size", type=int, default=64, help="Batch Size")
parser.add_argument("--num_epochs", type=int, default=30, help="Number of training epochs")
parser.add_argument("--log_to", type=str, default="wandb", help="Place to log metrics")
parser.add_argument("--save_dir", type=str, default="models/", help="Path to save trained best model")
parser.add_argument("--task_name", type=str, required=True, help="experiment name")


def run_training(task_name: str, data_dir: str, batch_size: int = 64, num_epochs: int = 30,
                 log_to: str = "wandb", save_dir="models/"):
    train_dataset = EmotionDataset(os.path.join(data_dir, "train.pkl"))
    test_dataset = EmotionDataset(os.path.join(data_dir, "test.pkl"))

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    loss = CrossEntropyLoss()
    model = resnest_cropped()
    optimizer = RAdam(model.parameters(), lr=0.001)
    lr_scheduler = ReduceLR(optimizer, mode="max", factor=0.5, patience=3)

    print("Total Params:", sum(p.numel() for p in model.parameters()))

    if log_to == "wandb":
        logger = wandb.init(
            project="TrainEmotionClassifier",
            name=task_name,
        )
    else:
        logger = None

    train(model, loss, optimizer, lr_scheduler, num_epochs, logger, save_dir, train_dataloader, test_dataloader)


if __name__ == "__main__":
    args = parser.parse_args()

    random_state = 42
    random.seed(random_state)
    os.environ["PYTHONHASHSEED"] = str(random_state)
    torch.manual_seed(random_state)
    np.random.seed(random_state)
    torch.cuda.manual_seed(random_state)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

    run_training(args.task_name, args.data_dir, args.batch_size, args.num_epochs, args.log_to, args.save_dir)
