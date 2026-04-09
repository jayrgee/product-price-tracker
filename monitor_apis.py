import re
from functools import partial
from pydoll.browser.tab import Tab
from pydoll.protocol.network.events import (
    NetworkEvent,
    ResponseReceivedEvent,
    RequestWillBeSentEvent,
)


async def log_api_request(api_path_regex: str, event: RequestWillBeSentEvent) -> None:
    params = event["params"]
    resource_type = params["type"]
    url = params["request"]["url"]

    api_types = ["Fetch", "XHR"]
    if resource_type not in api_types:
        return

    # Filter only API path calls
    if not re.search(api_path_regex, url):
        return

    request_id = params["requestId"]
    print(f"> {resource_type} Request: {request_id} : {url}")


async def capture_api_response(
    tab: Tab, api_path_regex: str, data_list: list, event: ResponseReceivedEvent
) -> None:
    params = event["params"]
    resource_type = params["type"]
    url = params["response"]["url"]

    api_types = ["Fetch", "XHR"]
    if resource_type not in api_types:
        return

    # Filter only API path calls
    if not re.search(api_path_regex, url):
        return

    request_id = params["requestId"]
    status = params["response"]["status"]

    print(f"< {resource_type} Response: {request_id} : {status} : {url}")

    try:
        body = await tab.get_network_response_body(request_id)
    except Exception as e:
        print(f"Failed to get response body: {e}")
        return

    data_list.append({"url": url, "body": body, "status": status})

    await tab.disable_network_events()


async def monitor_api_calls(tab: Tab, url: str, api_path: str) -> list[dict]:
    collected_data = []

    await tab.enable_network_events()
    await tab.on(
        NetworkEvent.REQUEST_WILL_BE_SENT,
        partial(log_api_request, api_path))
    await tab.on(
        NetworkEvent.RESPONSE_RECEIVED,
        partial(capture_api_response, tab, api_path, collected_data),
    )

    # Navigate to url
    await tab.go_to(url)

    return collected_data
