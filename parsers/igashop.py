from model import MerchantProduct


def parse_product(data: dict) -> MerchantProduct:
    """
    Parses product data from IGA.
    """
    return MerchantProduct(
        merchant="IGA",
        name=data["name"],
        brand=data["brand"],
        price=data["price"],
        was_price=data.get("wasPrice", ""),
        price_label=data.get("priceLabel", "")
    )