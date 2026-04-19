from model import MerchantProduct


def parse_product(data: dict) -> MerchantProduct:
    """
    Parses product data from Woolworths.
    """
    is_on_special = data.get("IsOnSpecial", False)

    return MerchantProduct(
        merchant="Woolworths",
        name=data["Name"],
        brand=data["Brand"],
        price=f"${data['Price']:.2f}",
        was_price=f"${data['WasPrice']:.2f}" if data.get("WasPrice") else "",
        price_label="On Special" if is_on_special else ""
    )