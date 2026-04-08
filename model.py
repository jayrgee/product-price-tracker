from abc import ABC

class MerchantProduct(ABC):
    """
    Base class representing a common product structure across different merchants.
    Provides getters and setters for all standard product properties.
    """
    @property
    def merchant(self) -> str:
        """The name of the merchant (e.g., Coles, Woolworths, IGA)."""
        return getattr(self, "_merchant", "")

    @merchant.setter
    def merchant(self, value: str) -> None:
        self._merchant = value

    @property
    def name(self) -> str:
        """The name of the product."""
        return getattr(self, "_name", "")

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def brand(self) -> str:
        """The brand name of the product."""
        return getattr(self, "_brand", "")

    @brand.setter
    def brand(self, value: str) -> None:
        self._brand = value

    @property
    def price(self) -> str:
        """The current price of the product (e.g., '$4.50')."""
        return getattr(self, "_price", "")

    @price.setter
    def price(self, value: str) -> None:
        self._price = value

    @property
    def was_price(self) -> str:
        """The previous price of the product if it is currently on special."""
        return getattr(self, "_was_price", "")

    @was_price.setter
    def was_price(self, value: str) -> None:
        self._was_price = value

    @property
    def price_label(self) -> str:
        """A label describing the price condition, such as 'On Special'."""
        return getattr(self, "_price_label", "")

    @price_label.setter
    def price_label(self, value: str) -> None:
        self._price_label = value

class ColesProduct(MerchantProduct):
    """
    Parses and represents product data from Coles.
    """
    def __init__(self, data) -> None:
        pricing_was = data["pricing"]["was"]
        price_description = data["pricing"]["priceDescription"]

        self.merchant = "Coles"
        self.name = data["name"]
        self.brand = data["brand"]
        self.price = f"${data["pricing"]["now"]:.2f}"
        self.was_price = f"${pricing_was:.2f}" if pricing_was else ""
        self.price_label = price_description if price_description else ""

class IgaProduct(MerchantProduct):
    """
    Parses and represents product data from IGA.
    """
    def __init__(self, data) -> None:
        self.merchant = "IGA"
        self.name = data["name"]
        self.brand = data["brand"]
        self.price = data["price"]
        self.was_price = data["wasPrice"]
        self.price_label = data["priceLabel"]

class WoolworthsProduct(MerchantProduct):
    """
    Parses and represents product data from Woolworths.
    """
    def __init__(self, data) -> None:
        is_on_special = data["IsOnSpecial"]

        self.merchant = "Woolworths"
        self.name = data["Name"]
        self.brand = data["Brand"]
        self.price = f"${data["Price"]:.2f}"
        self.was_price = f"${data["WasPrice"]:.2f}"
        self.price_label = "On Special" if is_on_special else ""

class ChemistWarehouseProduct(MerchantProduct):
    """
    Parses and represents product data from Chemist Warehouse.
    """
    def __init__(self, data) -> None:
        price = data["prices"][0]["price"]
        price_amount = price["value"]["amount"]
        price_rrp = price["rrp"]["amount"]

        product = data["product"]
        product_name = product["name"]
        product_variants = product["variants"][0]
        brand_label = product_variants["brand"]["label"]

        self.merchant = "Chemist Warehouse"
        self.name = product_name
        self.brand = brand_label
        self.price = f"${price_amount:.2f}"
        self.was_price = f"${price_rrp:.2f}"
        self.price_label = "On Special" if price_amount < price_rrp else ""
