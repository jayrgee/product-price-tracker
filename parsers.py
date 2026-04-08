from model import MerchantProduct

def parse_coles_product(data: dict) -> MerchantProduct:
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

def parse_iga_product(data: dict) -> MerchantProduct:
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

def parse_woolworths_product(data: dict) -> MerchantProduct:
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

def parse_chemist_warehouse_product(data: dict) -> MerchantProduct:
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
