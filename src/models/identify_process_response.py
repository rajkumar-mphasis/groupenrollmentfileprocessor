from __future__ import annotations

from dataclasses import dataclass, field

from src.models.additional_data import AdditionalData, create_additional_datas
from src.models.base import FromNodeBase
from src.models.offered_entity import Product


@dataclass
class IpResponse(FromNodeBase):
    gbp: str = ""
    products: list[Product] = field(default_factory=list)
    person_additional_data: list[AdditionalData] = field(default_factory=list)

    def init_from_node(self, node: dict, **kwargs) -> None:
        super().init_from_node(node, **kwargs)
        product_nodes = node["PossibleEnrollmentData"]["ProductChoices"]
        self.init_products(product_nodes)
        self.init_person_additional_data(product_nodes)

    def init_products(self, product_nodes):
        self.products = [Product.from_node(p) for p in product_nodes]

    def init_person_additional_data(self, product_nodes):
        # get first occurrence of insured
        if product_nodes:
            insured_node = product_nodes[0]["Options"][0]["Insured"]
            self.person_additional_data = create_additional_datas(
                insured_node["PersonAdditionalData"]
            )

    def display(
        self, parent_coverage=True, product_ads=True, insured_ads=True, person_ads=True
    ):
        print(f"GBP# {self.gbp}\n\n")
        if person_ads:
            print("Person additional data:")
            for ad in self.person_additional_data:
                print(" ", f"Pe_AD: {ad}")
            print()
        for p in self.products:
            p.display(parent_coverage, product_ads, insured_ads)
            print()
