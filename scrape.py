import asyncio
import json
from pydoll.browser.tab import Tab
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.constants import PageLoadState

from monitor_apis import monitor_api_calls
from stealth import set_headless, set_quick_stealth


async def get_next_product_data(tab: Tab) -> dict:
    """Extract product data from __NEXT_DATA__ page props"""

    # parse JSON from the DOM script tag with id "__NEXT_DATA__":
    product_data = await tab.execute_script(
        'return JSON.parse(document.querySelector("script#__NEXT_DATA__").innerText).props.pageProps.product',
        return_by_value=True,
    )
    # can also interrogate the global __NEXT_DATA__ object:
    # product_data = await tab.execute_script('return window.__NEXT_DATA__.props.pageProps.product', return_by_value=True)

    if "value" not in product_data["result"]["result"]:
        return {}

    return product_data["result"]["result"]["value"]

def get_chromium_options(is_headless: bool, is_api: bool) -> ChromiumOptions:

    #  https://pydoll.tech/docs/features/configuration/browser-options/?h=chromium
    options = ChromiumOptions()
    # options.add_argument('--incognito')  # Open in incognito mode
    if is_headless:
        set_headless(options)

    if is_api:
        set_quick_stealth(options=options)
        options.page_load_state = PageLoadState.COMPLETE # Wait for full page load to capture API calls
    else:
        options.page_load_state = PageLoadState.INTERACTIVE # Only require DOM access

    return options

async def _scrape_api(tab: Tab, url: str, api_path: str) -> list[dict]:
    pass

async def _srape_dom(tab: Tab, url: str) -> dict:
    pass

async def scrape_merchant_product(
    url: str, api_path: str | None, headless: bool = False
) -> None | dict:
    print(f"> url: {url}")

    options = get_chromium_options(is_headless=headless, is_api=bool(api_path))
    async with Chrome(options=options) as browser:
        tab = await browser.start()

        if api_path:
            data_list = await monitor_api_calls(tab, url, api_path)

            if not data_list:
                print("> No API calls captured.")
                return None

            # get first item in data_list and parse JSON
            item = data_list[0]
            json_data = item["body"]
            # Parse JSON
            api_data = json.loads(json_data)
            product_data = api_data["Product"]
        else:
            await tab.go_to(url)
            await asyncio.sleep(5)

            product_data = await get_next_product_data(tab)
            if not product_data:
                print("> No product data found in the page.")
                return None

        # json_data = json.dumps(product_data, indent=2)
        # print(f"Captured JSON: {json_data}")

        return product_data
