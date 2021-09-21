from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from src.models.additional_data import AdditionalData, create_additional_datas
from src.models.base import FromNodeBase


class InsuredType(Enum):
    OWNER = ""
    SPOUSE = "Spouse"
    CHILD = "Child"


class CoverageType(Enum):
    BASE = "Base"
    RIDER = "Rider"
    COVERAGEAMOUNTBUYUP = "CoverageAmountBuyUp"  # Not sure what it is used for


@dataclass
class OfferedEntity(FromNodeBase):
    name: str = ""
    code: str = ""
    # for Coverage additional_data are insured ad, no coverage ad beside mfactor in AFLAC context
    additional_data: list[AdditionalData] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name:<60} <{self.code}>"


@dataclass
class Coverage(OfferedEntity):
    external_coverage_code: str = ""
    coverage_type: CoverageType = CoverageType.BASE
    insured_type: InsuredType = InsuredType.OWNER
    parent: Optional[Coverage] = None

    def __str__(self) -> str:
        return super().__str__() + "    " + self.coverage_type.value

    def init_from_node(self, node: dict, **kwargs) -> None:
        super().init_from_node(node, **kwargs)
        self.name = node["Name"]
        self.code = node["Code"]
        self.external_coverage_code = node["ExternalCoverageCode"]
        self.coverage_type = CoverageType(node["CoverageType"])


CoveragesPerInsuredType = dict[InsuredType, list[Coverage]]


def init_coverage_additional_datas(
    insured_node: dict, coverages: list[Coverage]
) -> None:
    ads = create_additional_datas(insured_node["AdditionalData"])
    for ad in ads:
        # assert ad.coverage_code in (c.code for c in coverages)
        # false for <AG.AC.70.K.V.TMLF.C> in example
        for c in coverages:
            if c.code == ad.coverage_code:
                c.additional_data.append(ad)
                break


@dataclass
class Product(OfferedEntity):
    coverages: CoveragesPerInsuredType = field(
        default_factory=lambda: {i: [] for i in InsuredType}
    )

    def init_from_node(self, node: dict, **kwargs) -> None:
        super().init_from_node(node, **kwargs)
        product_node = node["Product"]
        self.name = product_node["Name"]
        self.code = product_node["Code"]
        self.init_coverages(node["Options"])
        self.init_additional_datas(product_node)

    def init_additional_datas(self, product_node: dict) -> None:
        self.additional_datas = create_additional_datas(product_node["AdditionalDatas"])

    def init_coverages(self, options_node: dict) -> None:
        for options_node in options_node:
            insured_node = options_node["Insured"]
            insured_type = InsuredType(insured_node["MainOwnerRelationshipToInsured"])
            inner_options_node = options_node["Options"]
            coverages = self.coverages[insured_type]
            for option_node_main in inner_options_node:
                option_node = option_node_main["Option"]
                parent_code = option_node_main["ParentOptionCode"]
                parent = None
                if parent_code:
                    # remove version <#n> from parent code
                    parent_code = parent_code.split("#")[0]
                    assert parent_code in (c.code for c in coverages)
                    parent = next(c for c in coverages if c.code == parent_code)
                cov = Coverage.from_node(
                    option_node, insured_type=insured_type, parent=parent
                )
                coverages.append(cov)
            init_coverage_additional_datas(insured_node, coverages)

    def display(self, parent_coverage=False, product_ads=False, insured_ads=False):
        print(f"PRODUCT: {self}")
        if product_ads:
            for ad in self.additional_datas:
                print(" ", f"Pr_AD: {ad}")
        for insured_type, coverages in self.coverages.items():
            print(" " * 3, insured_type)
            for c in coverages:
                print(" " * 7, f"COV: {c}")
                if parent_coverage and c.parent:
                    print(" " * 9, f"parent: <{c.parent.code}>")
                if insured_ads:
                    for ad in c.additional_data:
                        print(" " * 9, f"I_AD: {ad}")
