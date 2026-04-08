import asyncio
import tldextract
from dataclasses import dataclass

import parsers
from data import PRODUCT_DATA
from scrape import scrape_merchant_product

@dataclass
class Product:
    name: str
    urls: list[str]

def get_parser_for_url(url: str) -> None | callable:
    ext = tldextract.extract(url)
    domain = ext.domain
    parser_module = getattr(parsers, domain, None)
    if parser_module is None:
        print(f"> No parser found for domain: {domain}")
        return None

    parser = getattr(parser_module, "parse_product", None)
    if parser is None:
        print(f"> No parse_product function found in parser for domain: {domain}")
        return None

    return parser

def get_api_path_for_url(url: str) -> None | str:
    ext = tldextract.extract(url)
    domain = ext.domain
    match domain:
        case "woolworths":
            return '/apis/ui/product/detail/'
        case _:
            return None

async def process_product(product: Product) -> None:
    print(f"Product: {product['name']}")
    for url in product["urls"]:
        parser = get_parser_for_url(url)
        if parser is None:
            print(f"> No parser found for url: {url}")
            return
        api_path = get_api_path_for_url(url)
        product_data = await scrape_merchant_product(url, api_path)
        data = parser(product_data)
        data.display_product()

async def process_products(product_list: list[Product]) -> None:
    for product in product_list:
        await process_product(product)

async def main():
    await process_products(PRODUCT_DATA)

if __name__ == "__main__":
    asyncio.run(main())
