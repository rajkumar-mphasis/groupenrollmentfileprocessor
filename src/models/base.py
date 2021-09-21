from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="FromNodeBase")


@dataclass
class FromNodeBase:
    """
    Base class for dataclasses representing a node of a Wynsure API
    The self.node attribute is dictionary corresponding to JSON node in Wynsure
    Hold a reference to the node used to build the instance when the called API is an input
    Can build self.node from other attributes when the called API is an output
    """

    node: Optional[dict] = None

    def init_from_node(self, node: dict, **kwargs) -> None:
        self.node = node
        for name, value in kwargs.items():
            assert name in (f.name for f in fields(self))
            setattr(self, name, value)

    def build_node(self) -> None:
        self.node = None

    @classmethod
    def from_node(cls: Type[T], node: dict, **kwargs) -> T:
        inst = cls()
        inst.init_from_node(node, **kwargs)
        return inst
