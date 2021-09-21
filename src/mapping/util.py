from typing import Optional

from config.product_mapping import PRODUCT_MAPPING
from src.models.identify_process_response import IpResponse
from src.models.offered_entity import Product


def convert_date_format(date):
    """
    convert from YYYYMMDD to YYYY-MM-DD
    """
    if date == "" or date is None:
        return date
    return f"{date[:4]}-{date[4:6]}-{date[6:]}"


def find_corresponding_product(
    informatica_product_code: str, gbp_info: IpResponse
) -> Optional[Product]:
    code_candidates: list[str] = PRODUCT_MAPPING[informatica_product_code]
    for product in gbp_info.products:
        for code_candidate in code_candidates:
            if product.code.startswith(code_candidate):
                for data in product.coverages:
                    test = data
                return product
    return None
