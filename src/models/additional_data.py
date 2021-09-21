from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Optional, Type, TypeVar

from src.models.base import FromNodeBase

TDC = TypeVar("TDC", bound="AdditionalData")

additional_data_classes: dict[str, Type[AdditionalData]] = {}


def ad_register(classdef_name: str):
    """
    Decorate a given AdditionalData class:
     - Add it in additional_data_classes dict under <classdef_name> key
     - Set class var classdef_name from <classdef_name>
     - Add a custom __eq__ method
    Should be apply on all AdditionalData classes can be instantiated
    """

    def inner(cls: Type[TDC]) -> Type[TDC]:
        additional_data_classes[classdef_name] = cls
        setattr(cls, "classdef_name", classdef_name)
        setattr(cls, "__eq__", AdditionalData.__eq__)
        return cls

    return inner


@dataclass
class AdditionalData(FromNodeBase):
    """
    Base class for all AdditionalData
    With <self.value==None> it represents Wynsure FieldDesc (dynamic data & classifications)
    With a value it can be used to serialize a FieldValue in the payload
    """

    value: Any = None
    field_code: str = ""
    field_name: str = ""
    external_desc_code: str = ""
    coverage_code: str = ""

    def field_value(self):
        return self.value

    def init_from_node(self, node: dict, **kwargs) -> None:
        super().init_from_node(node, **kwargs)
        value_node, desc_node = node["Value"], node["Description"]
        self.init_from_value_node(value_node)
        self.init_from_desc_node(desc_node)
        self.coverage_code = node["CoverageCode"]

    def init_from_value_node(self, value_node: dict) -> None:
        self.field_code = value_node["FieldCode"]
        self.field_name = value_node["FieldName"]

    def init_from_desc_node(self, value_node: dict) -> None:
        pass

    def type_(self) -> str:
        return type(self).__name__.split(".")[-1].replace("AdditionalData", "")

    def __str__(self) -> str:
        return f"{self.field_name:<40} {self.field_code:<10} {self.type_()}"

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self.field_code == other.field_code
            and self.external_desc_code == other.external_desc_code
        )


@ad_register("aSPCB_AdditionalDataValue_Amount")
@dataclass
class AmountAdditionalData(AdditionalData):
    value: Decimal = Decimal("0.0")

    def field_value(self):
        return dict(Amount=self.value, Currency="USD")


@ad_register("aSPCB_AdditionalDataValue_CString")
@dataclass
class CStringAdditionalData(AdditionalData):
    value: str = ""


@ad_register("aSPCB_AdditionalDataValue_Text")
@dataclass
class TextAdditionalData(AdditionalData):
    value: str = ""


@ad_register("aAFCI_AdditionalDataValue_Float")
@dataclass
class FloatAdditionalData(AdditionalData):
    value: float = 0.0


@ad_register("aSPCB_AdditionalDataValue_Integer")
@dataclass
class IntAdditionalData(AdditionalData):
    value: int = 0


@ad_register("aSPCB_AdditionalDataValue_Date")
@dataclass
class DateAdditionalData(AdditionalData):
    value: Optional[date] = None

    def field_value(self):
        if self.value:
            return str(self.value)


@dataclass()
class ClassificationValue:
    my_owner: ClassificationAdditionalDataBase = field(compare=False)
    value_code: str
    field_value: str
    name_description: str


@dataclass
class ClassificationAdditionalDataBase(AdditionalData):
    """
    Base class for classification based additional data

    There is 2 types of classification based additional data in Wynsure which are functionally equivalent:
     - Pure classification (<aSPCB_ClassificationValue> in the payload)
     - Dynamic Data based on a classification (<aAFCI_ClassificationValueField> in the payload)
       In this case field code is different than the classification code
    """

    value: Optional[ClassificationValue] = None
    possible_values: list[ClassificationValue] = field(default_factory=list)

    # default_value: Optional[ClassificationValue] # probably not useful
    def init_from_desc_node(self, desc_node: dict) -> None:
        super().init_from_desc_node(desc_node)
        self.init_possible_values(desc_node)

    def init_possible_values(self, desc_node) -> None:
        if "PossibleValues" in desc_node:
            for v in desc_node["PossibleValues"]:
                self.possible_values.append(
                    ClassificationValue(
                        my_owner=self,
                        value_code=v["ValueCode"],
                        field_value=v["FieldValue"],
                        name_description=v["NameDescription"],
                    )
                )


@ad_register("aSPCB_ClassificationValue")
@dataclass
class ClassificationAdditionalData(ClassificationAdditionalDataBase):
    pass


@ad_register("aAFCI_ClassificationValueField")
@dataclass
class ClassificationFieldAdditionalData(ClassificationAdditionalDataBase):
    classification_code: str = ""
    classification_name: str = ""

    def init_from_desc_node(self, desc_node: dict) -> None:
        super().init_from_desc_node(desc_node)
        self.classification_code = desc_node["FieldCode"]
        self.classification_name = desc_node["FieldName"]


def create_additional_data(ad_node: dict) -> AdditionalData:
    assert "className" in ad_node
    assert ad_node["className"] == "aSPCB_AdditionalData_ValueDescription"
    assert "Description" in ad_node
    assert "Value" in ad_node
    value = ad_node["Value"]
    ad_class = additional_data_classes[value["className"]]
    return ad_class.from_node(ad_node)


def create_additional_datas(ad_node_list: list[dict]) -> list[AdditionalData]:
    ads: list[AdditionalData] = []
    for ad_node in ad_node_list:
        ad = create_additional_data(ad_node)
        # filter out separators
        if not ad.field_code.startswith("SEP_"):
            # filter out duplicate (same code and coverage code)
            if all(ad != o for o in ads):
                ads.append(ad)
    return ads
