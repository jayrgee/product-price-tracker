import json
from pydoll.browser.tab import Tab
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions

from monitor_apis import monitor_api_calls

async def get_next_product_data(tab: Tab) -> dict:
    """Extract product data from __NEXT_DATA__ page props"""

    # parse JSON from the script tag with id __NEXT_DATA__:
    # product_data = await tab.execute_script('return JSON.parse(document.querySelector("script#__NEXT_DATA__").innerText).props.pageProps.product', return_by_value=True)
    # can also interrogate the global __NEXT_DATA__ object:
    product_data = await tab.execute_script('return window.__NEXT_DATA__.props.pageProps.product', return_by_value=True)

    if "value" not in product_data['result']['result']:
        return {}

    return product_data['result']['result']['value']

async def scrape_merchant_product(url: str, api_path: str | None, headless: bool = False) -> None | dict:
    print(f"> url: {url}")

    #  https://pydoll.tech/docs/features/configuration/browser-options/?h=chromium
    options = ChromiumOptions()
    if headless:
        options.headless = True
        options.add_argument("--headless=new")  # More realistic headless mode
        options.add_argument("--enable-webgl")   # Bypasses hardware-check flags
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

    async with Chrome(options=options) as browser:
        tab = await browser.start()

        if api_path:
            data_list = await monitor_api_calls(tab, url, api_path)
            if not data_list:
                print("> No API calls captured.")
                return None

            # get first item in data_list and parse JSON
            item = data_list[0]
            json_data = item['body']
            # Parse JSON
            api_data = json.loads(json_data)
            product_data = api_data['Product']
        else:
            await tab.go_to(url)

            product_data = await get_next_product_data(tab)
            if not product_data:
                print("> No product data found in the page.")
                return None

        # json_data = json.dumps(product_data, indent=2)
        # print(f"Captured JSON: {json_data}")

        return product_data