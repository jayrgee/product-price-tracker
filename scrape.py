import asyncio
from collections.abc import Callable
import json
import logging
from pydoll.browser.tab import Tab
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.constants import PageLoadState

from monitor_apis import monitor_api_calls
from nextjs_data import get_nextjs_page_data
from stealth import set_headless, set_quick_stealth

logger = logging.getLogger(__name__)


def get_chromium_options(is_headless: bool, is_api: bool) -> ChromiumOptions:

    #  https://pydoll.tech/docs/features/configuration/browser-options/?h=chromium
    options = ChromiumOptions()
    if is_headless:
        set_headless(options)

    if is_api:
        set_quick_stealth(options=options)
        options.page_load_state = PageLoadState.COMPLETE  # Wait for full page load to capture API calls
    else:
        options.page_load_state = PageLoadState.INTERACTIVE  # Only require DOM access

    return options


async def _scrape_api(tab: Tab, url: str, api_path: str) -> list[dict]:
    pass


async def _srape_dom(tab: Tab, url: str) -> dict:
    pass


def _get_data_by_key(data: dict, key: str) -> dict:
    if key in data:
        return data[key]
    else:
        logger.warning(f"Key '{key}' not found in the data.")
        return {}

def _get_required_data(data: dict, data_filter: list[str]) -> dict:
    if not data_filter:
        return data

    if len(data_filter) == 1:
        key = data_filter[0]
        return _get_data_by_key(data, key)

    result = {}
    for key in data_filter:
        result[key] = _get_data_by_key(data, key)
    return result

async def scrape_merchant_product(url: str, options: dict, set_location_fn: Callable | None) -> None | dict:

    logger.info(f"url: {url}")
    api_path = options.get("api_path", None)
    is_headless = options.get("is_headless", False)
    data_filter = options.get("data_filter", None)
    location_options = options.get("location", None)
    base_url = options.get("base_url", None)

    chromiumOptions = get_chromium_options(is_headless=is_headless, is_api=bool(api_path))
    async with Chrome(options=chromiumOptions) as browser:
        tab = await browser.start()

        if location_options and set_location_fn:
            await tab.go_to(base_url)
            await asyncio.sleep(5)

            await set_location_fn(tab, location_options)

        if api_path:
            capture_list = await monitor_api_calls(tab, url, [api_path])

            if not capture_list:
                logger.warning("No API calls captured.")
                return None

            # get first item in capture_list and parse JSON
            item = capture_list[0]
            json_data = item["body"]
            # Parse JSON
            api_data = json.loads(json_data)
            product_data = _get_required_data(api_data, data_filter)
        else:
            await tab.go_to(url)
            await asyncio.sleep(5)

            page_data = await get_nextjs_page_data(tab)
            if not page_data:
                logger.warning("No nextjs page data found in the page")
                return None

            product_data = _get_required_data(page_data, data_filter)
            if not product_data:
                logger.warning("No product data found in the page.")
                return None

        # json_data = json.dumps(product_data, indent=2)
        # print(f"Captured JSON: {json_data}")

        return product_data
