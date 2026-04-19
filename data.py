PRODUCTS = [
    {
        "name": "Twinings Irish Breakfast Tea Bags 100 pack",
        "urls": [
            "https://www.woolworths.com.au/shop/productdetails/8647/twinings-irish-breakfast-tea-bags",
            "https://www.coles.com.au/product/twinings-irish-breakfast-tea-bags-100-pack-200g-83584",
            "https://www.igashop.com.au/product/twinings-irish-breakfast-tea-bags-32845"
        ]
    }
]

MERCHANTS = [
    {
        "name": "Chemist Warehouse",
        "base_url": "https://www.chemistwarehouse.com.au/",
        "api_path": None,
        "data_filter": ["product"]
    },
    {
        "name": "Coles",
        "base_url": "https://www.coles.com.au/",
        "api_path": None,
        "data_filter": ["product"]
    },
    {
        "name": "IGA",
        "base_url": "https://www.igashop.com.au/",
        "api_path": "api/storefront/stores/\d+/products/",
        "data_filter": [],
        "location": {
            "location_url": "https://www.igashop.com.au/",
            "location_input_selector": "input#search-location",
            "location_input_value": "3000",
            "location_api": "/api/storefront/stores\?RSID",
            "location_filter": []
        }
    },
    {
        "name": "Woolworths",
        "base_url": "https://www.woolworths.com.au/",
        "api_path": "/apis/ui/product/detail/",
        "data_filter": ["Product"]
    }
]
