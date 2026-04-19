import asyncio
import logging
import re
from functools import partial
from pydoll.browser.tab import Tab
from pydoll.protocol.network.events import (
    NetworkEvent,
    ResponseReceivedEvent,
    RequestWillBeSentEvent,
)
from pydoll.protocol.network.types import ResourceType

logger = logging.getLogger(__name__)

API_RESOURCE_TYPES = [ResourceType.FETCH, ResourceType.XHR]

async def log_api_request(api_regex_paths: list[str], event: RequestWillBeSentEvent) -> None:
    params = event["params"]
    resource_type = params["type"]
    url = params["request"]["url"]

    if resource_type not in API_RESOURCE_TYPES:
        return

    # Filter only API path calls
    # if none of the api_paths match the url, return
    if not any(re.search(api_regex, url) for api_regex in api_regex_paths):
        return

    request_id = params["requestId"]
    logger.info(f"> {resource_type} Request: {request_id} : {url}")


async def capture_api_response(
    tab: Tab, api_regex_paths: list[str], data_list: list, event: ResponseReceivedEvent
) -> None:
    params = event["params"]
    resource_type = params["type"]
    url = params["response"]["url"]

    if resource_type not in API_RESOURCE_TYPES:
        return

    # Filter only API path calls
    # if none of the api_paths match the url, return
    if not any(re.search(api_regex, url) for api_regex in api_regex_paths):
        return

    request_id = params["requestId"]
    status = params["response"]["status"]

    logger.info(f"< {resource_type} Response: {request_id} : {status} : {url}")

    if 200 <= status < 300:
        try:
            body = await tab.get_network_response_body(request_id)
        except Exception as e:
            logger.error(f"Failed to get response body: {e}")
            return

        data_list.append({"url": url, "body": body, "status": status})

        await tab.disable_network_events()


async def monitor_api_calls(tab: Tab, url: str, api_paths: list[str]) -> list[dict]:
    collected_data = []

    await tab.enable_network_events()
    # Set up listeners for API calls matching any of the specified API paths
    # for api_path in api_paths:
    await tab.on(
        NetworkEvent.REQUEST_WILL_BE_SENT,
        partial(log_api_request, api_paths)
    )
    await tab.on(
        NetworkEvent.RESPONSE_RECEIVED,
        partial(capture_api_response, tab, api_paths, collected_data),
    )

    # Navigate to url
    await tab.go_to(url)
    await asyncio.sleep(5)  # Wait for API calls to complete

    return collected_data
