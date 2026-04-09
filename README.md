# Product Price Tracker

A Python project designed to track and normalize product pricing data from various Australian retail websites, including Coles, Woolworths, IGA, and Chemist Warehouse.

## Description

This project scrapes product pages and APIs from major Australian retailers (merchants) to extract key pricing information. Because each retailer has a unique web or API response structure, the application parses raw data into a common `MerchantProduct` using a `parse_product` parser function to make price comparison uniform and straightforward.

`MerchantProduct` contains standard details such as:
- **Merchant:** Retailer name (e.g., Coles, Woolworths, IGA)
- **Name:** The product's clear name
- **Brand:** The product's brand
- **Price:** The current price
- **Was Price:** The previous price (if the item is currently on special)
- **Price Label:** Any specific pricing label or condition (e.g., "On Special")

## Installation

1. **Install Python**: Python 3.14 or newer is required. Download it from [python.org](https://www.python.org/downloads/) or install via your system's package manager.

2. **Install `uv`**:
   - [uv](https://docs.astral.sh/uv/) is an extremely fast Python package and project manager.
   - https://docs.astral.sh/uv/#installation

3. **Sync Project Dependencies**:
   Call `uv sync`to sync the project's dependencies.
   ```bash
   uv sync
   ```

4. **Run the Project**:
   Call `uv run` to  execute the project's entry point:
   ```bash
   # run project
   uv run main.py

   # run project in headless mode
   uv run main.py --headless
   ```

5. **Linting**
   ```bash
   # Format code with ruff
   uv run ruff format .

   # Run linting with automated fixes
   uv run ruff check --fix .
   ```