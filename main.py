import asyncio
from collections.abc import Callable
import logging
import sys
import tldextract
from dataclasses import dataclass

import constants
import merchants
from data import PRODUCTS, MERCHANTS
from scrape import scrape_merchant_product

@dataclass
class Product:
    name: str
    urls: list[str]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')


def get_domain_from_url(url: str) -> str:
    ext = tldextract.extract(url)
    return ext.domain

def get_merchant_function(merchant_domain: str, function_name: str) -> None | Callable:
    merchant_module = getattr(merchants, merchant_domain, None)
    if merchant_module is None:
        logger.warning(f"> No merchant module found for domain: {merchant_domain}")
        return None

    fn: Callable | None = getattr(merchant_module, function_name, None)
    if fn is None:
        logger.warning(f"> No '{function_name}' function found in merchant module for domain: {merchant_domain}")
        return None

    return fn

def get_merchant_for_url(url: str) -> dict | None:
    """Determine merchant from URL"""

    # Each merchant has a base URL defined in MERCHANTS data
    # If the URL matches a merchant's base URL, return the corresponding merchant object
    merchant = next((m for m in MERCHANTS if url.startswith(m['base_url'])), None)
    if merchant:
        return merchant
    return None

async def process_product(product: Product, headless: bool = False) -> None:
    logger.info(f"Product: {product['name']}")
    for url in product["urls"]:
        domain = get_domain_from_url(url)
        parser_fn = get_merchant_function(domain, constants.PARSE_PRODUCT_FUNCTION_NAME)
        if parser_fn is None:
            logger.warning(f"> No parser found for url: {url}")
            continue

        merchant = get_merchant_for_url(url)
        if merchant is None:
            logger.warning(f"> No merchant found for url: {url}")
            continue

        location_options = merchant.get("location", None)
        if location_options:
            # set reference to set_location function in merchant module
            set_location_fn = get_merchant_function(domain, constants.SET_LOCATION_FUNCTION_NAME)
        else:
            set_location_fn = None

        options = {
            "is_headless": headless,
            "api_path": merchant.get("api_path", None),
            "data_filter": merchant.get("data_filter", None),
            "location": location_options,
            "base_url": merchant.get("base_url", None)
        }

        product_data = await scrape_merchant_product(url, options, set_location_fn)
        if product_data is None:
            logger.warning(f"> No product data found for url: {url}")
            continue

        data = parser_fn(product_data)
        data.display_product()

async def process_products(product_list: list[Product], headless: bool = False) -> None:
    for product in product_list:
        await process_product(product, headless)

async def main(headless: bool = False) -> None:
    await process_products(PRODUCTS, headless)

if __name__ == "__main__":
    args = sys.argv[1:]
    logger.info(f"Arguments: {args}")
    headless = True if "--headless" in args else False
    asyncio.run(main(headless))
