""" Deep Learning Package for Python

boris is a Python module for self-supervised active learning.

"""

from ._one_liners import train_model_and_get_image_features
from ._one_liners import train_self_supervised_model
from ._one_liners import get_image_features

__version__ = '0.0.dev0'

__all__ = [
    'cli',
    'api',
    'data',
    'embedding',
    'loss',
    'models',
    'sampling'
    'transforms',
    'utils',
]
