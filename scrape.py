import asyncio
import json
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions

from model import ChemistWarehouseProduct, ColesProduct, IgaProduct, MerchantProduct, WoolworthsProduct
from monitor_apis import monitor_api_calls

def display_product(product: MerchantProduct) -> None:
    print(f"Merchant: {product.merchant}")
    print(f"Name: {product.name}")
    print(f"Brand: {product.brand}")
    print(f"Price: {product.price}")
    if product.was_price:
        print(f"Was Price: {product.was_price}")
    if product.price_label:
        print(f"Price Label: {product.price_label}")

async def scrape_url(url: str) -> None:
    print(f"> {url=}")

    #  https://pydoll.tech/docs/features/configuration/browser-options/?h=chromium
    options = ChromiumOptions()
    async with Chrome(options=options) as browser:
        tab = await browser.start()

        if "woolworths" in url:
            api_path = '/apis/ui/product/detail/'
            data_list = await monitor_api_calls(tab, url, api_path)
            await tab.go_to(url)
            # get first item in data_list and parse JSON
            if not data_list:
                print("> No API calls captured.")
                return

            item = data_list[0]
            json_data = item['body']
            # Parse JSON
            api_data = json.loads(json_data)
            data = WoolworthsProduct(api_data['Product'])
            display_product(data)
        else:
            data_list = await monitor_api_calls(tab, url, "fubardle") # Use a non-matching regex to skip API capture for Coles and IGA
            await tab.go_to(url)
            await asyncio.sleep(5)

            product_data = await tab.execute_script('return window.__NEXT_DATA__.props.pageProps.product', return_by_value=True)

            if "value" not in product_data['result']['result']:
                print("> No product data found in the page.")
                return

            product_data_result_value = product_data['result']['result']['value']

            json_data = json.dumps(product_data_result_value, indent=2)
            # print(f"Captured JSON: {json_data}")

            if "chemistwarehouse" in url:
                data = ChemistWarehouseProduct(product_data_result_value)
                display_product(data)

            if "coles" in url:
                data = ColesProduct(product_data_result_value)
                display_product(data)

            if "igashop" in url:
                data = IgaProduct(product_data_result_value)
                display_product(data)

        await asyncio.sleep(5)
