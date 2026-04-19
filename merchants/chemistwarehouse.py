from model import MerchantProduct


def parse_product(data: dict) -> MerchantProduct:
    """
    Parses product data from Chemist Warehouse.
    """
    price = data["prices"][0]["price"]
    price_amount = price["value"]["amount"]
    price_rrp = price["rrp"]["amount"]

    product = data["product"]
    product_name = product["name"]
    product_variants = product["variants"][0]
    brand_label = product_variants["brand"]["label"]

    return MerchantProduct(
        merchant="Chemist Warehouse",
        name=product_name,
        brand=brand_label,
        price=f"${price_amount:.2f}",
        was_price=f"${price_rrp:.2f}" if price_rrp else "",
        price_label="On Special" if price_amount < price_rrp else ""
    )