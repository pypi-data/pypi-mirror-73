# -*- coding: utf-8 -*-
"""
    boris-cli
    ~~~~~~~~~

    A simple command line tool to train a state-of-the-art
    self-supervised model on your image dataset.

"""

import hydra

from boris.data import ImageCollateFunction
from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.loss import NTXentLoss
from boris.models import ResNetSimCLR
from boris.cli._helpers import fix_input_path

import torch


def _train_cli(cfg, is_cli_call=True):
    """Train a self-supervised model on the image dataset of your choice.

    Args:
        cfg[data]: (str)
            Name of the dataset (to download use cifar10 or cifar100)
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str)
            If specified, the dataset is loaded from the folder

    Returns:
        checkpoint: (str) Path to checkpoint of the best model during training

    """

    data = cfg['data']
    download = cfg['download']

    root = cfg['root']
    if root and is_cli_call:
        root = fix_input_path(root)

    from_folder = cfg['from_folder']
    if from_folder and is_cli_call:
        from_folder = fix_input_path(from_folder)

    if 'seed' in cfg.keys():
        seed = cfg['seed']
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    if cfg['trainer'] and cfg['trainer']['gpus']:
        if not torch.cuda.is_available():
            cfg['trainer']['gpus'] = 0

    model = ResNetSimCLR(**cfg['model'])
    criterion = NTXentLoss(**cfg['criterion'])

    optimizer = torch.optim.SGD(model.parameters(), **cfg['optimizer'])

    dataset = BorisDataset(root,
                           name=data, train=True, download=download,
                           from_folder=from_folder)

    collate_fn = ImageCollateFunction(**cfg['collate'])
    dataloader = torch.utils.data.DataLoader(dataset,
                                             **cfg['loader'],
                                             collate_fn=collate_fn)

    encoder = SelfSupervisedEmbedding(model, criterion, optimizer, dataloader)
    encoder = encoder.train(**cfg['trainer'])

    print('Best model is stored at: %s' % (encoder.checkpoint))
    return encoder.checkpoint


@hydra.main(config_path="config/config.yaml", strict=False)
def train_cli(cfg):
    """Train a self-supervised model on the image dataset of your choice.

    Args:
        cfg[data]: (str)
            Name of the dataset (to download use cifar10 or cifar100)
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str)
            If specified, the dataset is loaded from the folder

    Returns:
        checkpoint: (str) Path to checkpoint of the best model during training

    """

    return _train_cli(cfg)


def entry():
    train_cli()
