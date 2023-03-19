# Standard library imports
import time

# Third-party library imports
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc

# Constants
STEAMDB_URL = "https://steamdb.info/sales/?cc=ar&min_reviews=0&min_rating=0&min_discount=0&category=29"
STEAM_STORE_CART_URL = "https://store.steampowered.com/cart/"
TWO_YEAR_LOWS_SELECTOR = "#js-discounts-minor > div"
PRICE_COLUMN_SELECTOR = "#DataTables_Table_0 > thead > tr > th:nth-child(5)"

opts = ChromeOptions()
opts.add_argument("--window-size=1800,1400")
opts.add_argument("--user-data-dir=C:\\Users\\vasya\\AppData\\Local\\Google_2\\Chrome\\User Data")
opts.add_argument('--profile-directory=Profile 69')

driver = uc.Chrome(options=opts)
driver.get(STEAMDB_URL)

def filter_2_year_lows(driver):
    filter_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, TWO_YEAR_LOWS_SELECTOR)))
    filter_button.click()

def sort_by_price(driver):
    sort_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRICE_COLUMN_SELECTOR))
    )
    sort_button.click()

def get_sale_price(driver, sale_index):
    SALE_PRICE_SELECTOR = f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(5)"
    sale_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SALE_PRICE_SELECTOR)))
    sale_price = float(sale_price_element.text.replace("ARS$ ", "").replace(',', '.'))
    return sale_price

def click_sale_link(driver, sale_index):
    SALE_LINK_SELECTOR = f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(1) > a"
    sale_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SALE_LINK_SELECTOR)))
    sale_link.click()

def add_to_cart(driver, sale_index, max_price, total_sum):
    sale_price = get_sale_price(driver, sale_index)

    if sale_price < max_price:
        if total_sum + sale_price > max_total_sum:
            print(f"Sale {sale_index}: Sale price is ARS$ {sale_price}, Total sum would exceed the max total sum, skipping...")
            return total_sum
        else:
            total_sum += sale_price
            print(f"Sale {sale_index}: Sale price is ARS$ {sale_price}, Total sum: ARS$ {total_sum:.2f}")
    else:
        print(f"Sale {sale_index}: Sale price is ARS$ {sale_price}, Total sum: ARS$ {total_sum:.2f}")
        return total_sum

    if sale_price >= max_price:
        print(f"Sale {sale_index} is above the price threshold, skipping...")
        return

    click_sale_link(driver, sale_index)
    driver.switch_to.window(driver.window_handles[1])

    if total_sum < max_total_sum:
        total_sum = handle_add_to_cart_process(driver, sale_index, total_sum)
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return total_sum

def handle_add_to_cart_process(driver,sale_index, total_sum):
    ADD_TO_CART_SELECTOR = "a[id^='btn_add_to_cart_'] > span"

    try:
        add_to_cart_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ADD_TO_CART_SELECTOR)))
        if "In Cart" in add_to_cart_button.get_attribute("innerHTML"):
            print(f"Sale {sale_index} is already in the cart")
        else:
            add_to_cart_button.click()
            WebDriverWait(driver, 1).until(EC.url_matches(STEAM_STORE_CART_URL))
    except TimeoutException:
        print(f"Sale {sale_index} is already in the cart or not available")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return total_sum

num_sales_to_add = 30
max_price = 50
max_total_sum = 122

filter_2_year_lows(driver)
sort_by_price(driver)

num_sales_added = 0
total_sum = 0
for i in range(1, num_sales_to_add + 1):
    previous_sum = total_sum
    total_sum = add_to_cart(driver, i, max_price, total_sum)
    # If the total_sum has increased, increment the num_sales_added counter
    if total_sum > previous_sum:
        num_sales_added += 1

# Print the final values for num_sales_added and total_sum after the loop
print(f"\nNumber of sales added: {num_sales_added}")
print(f"Total price of sales added: ARS$ {total_sum:.2f}\n")

driver.switch_to.new_window('tab')
driver.get(STEAM_STORE_CART_URL)
input("Press enter to close the browser...")

# Close the browser
driver.quit()

