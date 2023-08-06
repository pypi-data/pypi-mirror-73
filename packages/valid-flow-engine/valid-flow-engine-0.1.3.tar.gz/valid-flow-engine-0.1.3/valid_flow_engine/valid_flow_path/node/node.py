from __future__ import annotations
import typing
from abc import ABC, abstractmethod


class Node(ABC):
    """Base Class for all Nodes

    Arguments:
        ABC {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    @property
    def id(self):
        return self._id
