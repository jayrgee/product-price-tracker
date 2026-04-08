import json
import tldextract
from pydoll.browser.tab import Tab
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions

import parsers
from monitor_apis import monitor_api_calls

def get_parser_for_domain(domain: str):
    parser_module = getattr(parsers, domain, None)
    if parser_module is None:
        print(f"> No parser found for domain: {domain}")
        return None

    parser = getattr(parser_module, "parse_product", None)
    if parser is None:
        print(f"> No parse_product function found in parser for domain: {domain}")
        return None

    return parser

async def get_next_product_data(tab: Tab) -> dict:
    """Extract product data from __NEXT_DATA__ page props"""

    # parse JSON from the script tag with id __NEXT_DATA__:
    # product_data = await tab.execute_script('return JSON.parse(document.querySelector("script#__NEXT_DATA__").innerText).props.pageProps.product', return_by_value=True)
    # can also interrogate the global __NEXT_DATA__ object:
    product_data = await tab.execute_script('return window.__NEXT_DATA__.props.pageProps.product', return_by_value=True)

    if "value" not in product_data['result']['result']:
        return {}

    return product_data['result']['result']['value']

async def scrape_url(url: str) -> None:
    print(f"> url: {url}")

    ext = tldextract.extract(url)
    domain = ext.domain
    print(f"> domain: {domain}")

    parser = get_parser_for_domain(domain)
    if parser is None:
        print(f"> No parser found for domain: {domain}")
        return

    #  https://pydoll.tech/docs/features/configuration/browser-options/?h=chromium
    options = ChromiumOptions()
    async with Chrome(options=options) as browser:
        tab = await browser.start()

        if domain == "woolworths":
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
            product_data = api_data['Product']
        else:
            await tab.go_to(url)

            product_data = await get_next_product_data(tab)
            if not product_data:
                print("> No product data found in the page.")
                return

        # json_data = json.dumps(product_data, indent=2)
        # print(f"Captured JSON: {json_data}")

        data = parser(product_data)
        data.display_product()
