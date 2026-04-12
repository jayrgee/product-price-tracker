from pydoll.browser.tab import Tab

def _extract_cdp_value(response):
    """Extract the actual value from a CDP (Chrome DevTools Protocol) response."""
    if isinstance(response, dict):
        return response.get('result', {}).get('result', {}).get('value', '')
    return response

async def get_nextjs_page_data(tab: Tab, getGlobal: bool = True) -> dict:
    """Gets data from global __NEXT_DATA__ page props object"""

    # NextJS apps often embed page data in a script element with id "__NEXT_DATA__".
    # This element contains a JSON object with all the data used to render the page.
    # On initialization, this data is available in the global window.__NEXT_DATA__ variable.
    # By executing JavaScript in the page context, we can extract this data without needing to monitor API calls.
    # The following code uses an Immediately Invoked Function Expression (IIFE) to safely access the JSON data:

    if getGlobal:
        js_iife = """
            (() => {
                const nextData = window.__NEXT_DATA__;
                if (!nextData || !nextData.props || !nextData.props.pageProps) { return {}; }
                return nextData.props.pageProps;
            })()
            """
    else:
        js_iife = """
            (() => {
                const nextDataElement = document.getElementById('__NEXT_DATA__');
                let nextData;
                if (nextDataElement) {
                    try {
                        nextData = JSON.parse(nextDataElement.textContent);
                    } catch (e) {
                        return {};
                    }
                }
                if (!nextData || !nextData.props || !nextData.props.pageProps) { return {}; }
                return nextData.props.pageProps;
            })()
            """
    cdp_response = await tab.execute_script(js_iife, return_by_value=True) # returns a CDP response object
    page_data = _extract_cdp_value(cdp_response)

    if not page_data:
        return {}

    return page_data
