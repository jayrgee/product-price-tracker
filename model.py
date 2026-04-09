from dataclasses import dataclass

@dataclass
class MerchantProduct:
    """
    Representation of a common product structure across different merchants.
    """
    merchant: str
    name: str
    brand: str
    price: str
    was_price: str = ""
    price_label: str = ""

    def display_product(self) -> None:
        print(f"- Merchant: {self.merchant}")
        print(f"- Name: {self.name}")
        print(f"- Brand: {self.brand}")
        print(f"- Price: {self.price}")
        if self.was_price:
            print(f"- Was Price: {self.was_price}")
        if self.price_label:
            print(f"- Price Label: {self.price_label}")
