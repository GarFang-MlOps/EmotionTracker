import os.path

import numpy as np
import torch
from torch.nn.functional import softmax
from torchmetrics import Accuracy
from tqdm import tqdm

from model.config import CLASS_MAPPING


def train(model, loss, optimizer, lr_scheduler, num_epochs, logger, save_dir, train_loader, test_loader):
    device = "cuda"
    best_metric = -1
    model.to(device)

    for _ in tqdm(range(num_epochs)):
        model.train()

        for images, targets in train_loader:
            optimizer.zero_grad()
            images_cuda = images.to(device)
            targets_cuda = targets.to(device)
            output = softmax(model(images_cuda), dim=1)
            loss_ = loss(output, targets_cuda)
            loss_.backward()
            logger.log({"loss": loss_.item()})
            optimizer.step()

        epoch_metric = eval(model, test_loader, logger)
        logger.log({"LR": optimizer.param_groups[0]["lr"]})

        if epoch_metric > best_metric:
            torch.save({"state": model.state_dict()}, os.path.join(save_dir, "model_best.pkl"))
            best_metric = epoch_metric

        reduce = lr_scheduler.step(epoch_metric)
        if reduce:
            model.load_state_dict(torch.load(os.path.join(save_dir, "model_best.pkl"))["state"])
            print("Reduced LR")


def eval(model, test_loader, logger):
    model.eval()
    device = "cuda"
    accuracy_macro = Accuracy(task="multiclass", average="macro", num_classes=len(CLASS_MAPPING))
    accuracy_micro = Accuracy(task="multiclass", average="micro", num_classes=len(CLASS_MAPPING))
    targets_full = []
    predicts_full = []
    with torch.no_grad():
        for images, targets in tqdm(test_loader):
            images_cuda = images.to(device)
            targets = torch.argmax(targets, dim=1)
            output = torch.argmax(model(images_cuda), dim=1)
            targets_full.extend(targets)
            predicts_full.extend(output)

    accuracy_macro_res = accuracy_macro(torch.tensor(predicts_full), torch.tensor(targets_full))
    accuracy_micro_res = accuracy_micro(torch.tensor(predicts_full), torch.tensor(targets_full))
    logger.log({"Macro Accuracy": accuracy_macro_res})
    logger.log({"Micro Accuracy": accuracy_micro_res})
    return accuracy_macro_res
