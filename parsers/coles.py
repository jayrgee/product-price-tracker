from model import MerchantProduct


def parse_product(data: dict) -> MerchantProduct:
    """
    Parses product data from Coles.
    """
    pricing_was = data["pricing"].get("was")
    price_description = data["pricing"].get("priceDescription")

    return MerchantProduct(
        merchant="Coles",
        name=data["name"],
        brand=data["brand"],
        price=f"${data['pricing']['now']:.2f}",
        was_price=f"${pricing_was:.2f}" if pricing_was else "",
        price_label=price_description if price_description else ""
    )