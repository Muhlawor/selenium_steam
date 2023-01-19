# selenium_steam

This repository contains a Python script that uses Selenium and the Chrome webdriver to scrape Steam sales data and automate the process of adding items to a cart.

## Prerequisites
- Selenium
- Chrome webdriver
- undetected_chromedriver
- Chrome browser

## Usage
1. Clone the repository
2. Install the necessary packages by running `pip install -r requirements.txt`
3. Update the `user-data-dir` argument in the `opts` variable to match the location of your Chrome user data.
4. Run the script with `python main_optimized.py`

## Functionality
- The script navigates to a specific Steam sales page and filters the results to show 2-year lows
- It then sorts the sales by price
- The script then adds the first 50 items to the cart

**Note**: The script uses a sleep time of 1 second between adding items to the cart to reduce the chance of being blocked by Steam. As well as a sleep time of 999 second at the end of the script to keep the browser open and check the results.