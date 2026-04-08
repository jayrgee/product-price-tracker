import asyncio
from dataclasses import dataclass

from data import PRODUCT_DATA
from scrape import scrape_url

@dataclass
class Product:
    name: str
    urls: list[str]


async def process_product(product: Product) -> None:
    print(f"Product: {product['name']}")
    for url in product["urls"]:
        await scrape_url(url)

async def process_products(product_list: list[Product]) -> None:
    for product in product_list:
        await process_product(product)

async def main():
    await process_products(PRODUCT_DATA)

if __name__ == "__main__":
    asyncio.run(main())
