import asyncio
import re
from functools import partial
from pydoll.browser.tab import Tab
from pydoll.protocol.network.events import NetworkEvent, ResponseReceivedEvent

async def monitor_api_calls(tab: Tab, url: str, api_path: str) -> list[dict]:
    collected_data = []

    # Type hint helps IDE autocomplete event keys
    async def capture_api_response(tab: Tab, api_path_regex: str, data_list: list, event: ResponseReceivedEvent):
        params = event['params']
        resource_type = params['type']
        url = params['response']['url']

        api_types = ['Fetch', 'XHR']
        if resource_type not in api_types:
            return

        # Filter only API path calls
        if not re.search(api_path_regex, url):
            return

        request_id = params['requestId']
        status = params['response']['status']

        try:
            body = await tab.get_network_response_body(request_id)
        except Exception as e:
            print(f"Failed to get response body: {e}")
            return

        data_list.append({
            'url': url,
            'body': body,
            'status': status
        })
        # print(f"Captured API call {status}: {url}")

    await tab.enable_network_events()
    await tab.on(
        NetworkEvent.RESPONSE_RECEIVED,
        partial(capture_api_response, tab, api_path, collected_data)
    )

    # Navigate and collect
    await tab.go_to(url)

    await asyncio.sleep(3)  # Wait for requests to complete

    return collected_data