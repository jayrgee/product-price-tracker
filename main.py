import asyncio
import sys
import tldextract
from dataclasses import dataclass

import constants
import parsers
from data import PRODUCTS, MERCHANTS
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

    parser = getattr(parser_module, constants.PARSE_FUNCTION_NAME, None)
    if parser is None:
        print(f"> No '{constants.PARSE_FUNCTION_NAME}' function found in parser for domain: {domain}")
        return None

    return parser

def get_api_path_for_url(url: str) -> None | str:
    """Determine API path based on Merchant base URL"""

    # Each merchant has a base URL and an optional API path defined in MERCHANTS data
    # If the URL matches a merchant's base URL, return the corresponding API path
    merchant = next((m for m in MERCHANTS if url.startswith(m['base_url'])), None)
    if merchant:
        return merchant['api_path']
    return None

async def process_product(product: Product, headless: bool = False) -> None:
    print(f"Product: {product['name']}")
    for url in product["urls"]:
        parser = get_parser_for_url(url)
        if parser is None:
            print(f"> No parser found for url: {url}")
            continue

        api_path = get_api_path_for_url(url)
        product_data = await scrape_merchant_product(url, api_path, headless)
        if product_data is None:
            print(f"> No product data found for url: {url}")
            continue

        data = parser(product_data)
        data.display_product()

async def process_products(product_list: list[Product], headless: bool = False) -> None:
    for product in product_list:
        await process_product(product, headless)

async def main(headless: bool = False) -> None:
    await process_products(PRODUCTS, headless)

if __name__ == "__main__":
    args = sys.argv[1:]
    print(f"Arguments: {args}")
    headless = True if "--headless" in args else False
    asyncio.run(main(headless))
