import logging
from pydoll.browser.tab import Tab
from model import MerchantProduct

TIMEOUT_SECONDS = 30

logger = logging.getLogger(__name__)


def parse_product(data: dict) -> MerchantProduct:
    """
    Parses product data from IGA.
    """
    return MerchantProduct(
        merchant="IGA",
        name=data["name"],
        brand=data["brand"],
        price=data["price"],
        was_price=data.get("wasPrice", ""),
        price_label=data.get("priceLabel", ""),
    )


async def set_location(tab: Tab, location_options: dict) -> None:
    """Set location for IGA"""

    location_input_selector = location_options.get("location_input_selector")
    location_input_value = location_options.get("location_input_value")

    input_element = await tab.query(
        location_input_selector, raise_exc=False, timeout=TIMEOUT_SECONDS
    )
    if input_element:
        await input_element.focus()
        await input_element.type_text(location_input_value, humanize=True)

        # get id of result list and click first result
        loc_item_selector = "ul[data-test-id='address-finder-location-list'] div"
        loc_item_element = await tab.query(
            loc_item_selector, raise_exc=False, timeout=TIMEOUT_SECONDS
        )
        if loc_item_element:
            await loc_item_element.click()

            store_item_selector = (
                "div[data-test-id='store-selection-list-item']:first-child button"
            )
            store_item_element = await tab.query(
                store_item_selector, raise_exc=False, timeout=TIMEOUT_SECONDS
            )
            if store_item_element:
                await store_item_element.click()
            else:
                logger.warning(
                    f"No store results found for selector: {store_item_selector}"
                )
        else:
            logger.warning(
                f"No location results found for selector: {loc_item_selector}"
            )
