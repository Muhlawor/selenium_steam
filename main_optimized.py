import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc

opts = ChromeOptions()
opts.add_argument("--window-size=1800,1400")
opts.add_argument("--user-data-dir=C:\\Users\\vasya\\AppData\\Local\\Google_2\\Chrome\\User Data")
opts.add_argument('--profile-directory=Profile 69')

driver = uc.Chrome(options=opts)

# Navigate to the website
driver.get("https://steamdb.info/sales/?cc=ar&min_reviews=0&min_rating=0&min_discount=0&category=29")


# time.sleep(999)
# Function to filter the sales by 2 year lows
def filter_2_year_lows():
    filter_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#js-discounts-minor > div")))
    filter_button.click()


# Function to sort the sales by price
def sort_by_price():
    sort_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#DataTables_Table_0 > thead > tr > th:nth-child(5)")))
    sort_button.click()


# Function to add a specific sale to the cart based on price
def add_to_cart(sale_index):
    sale_price = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                  f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(5)"))).text

    sale_price = float(sale_price.replace("ARS$ ", "").replace(',', '.'))

    if sale_price >= max_price:
        print(f"Sale {sale_index} is above the price threshold, skipping...")
        return

    sale_link = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                 f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(1) > a")))
    sale_link.click()
    driver.switch_to.window(driver.window_handles[1])
    try:
        add_to_cart_button = WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a[id^='btn_add_to_cart_'] > span")))
        if "In Cart" in add_to_cart_button.get_attribute("innerHTML"):
            print(f"Sale {sale_index} is already in the cart")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return
        add_to_cart_button.click()
    except TimeoutException:
        print(f"Sale {sale_index} is already in the cart")
    try:
        WebDriverWait(driver, 1).until(expected_conditions.url_matches("https://store.steampowered.com/cart/"))
    except TimeoutException:
        print("pass")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])




# Amount of games to add
num_sales_to_add = 50
# Maximum price of game to add
max_price = 50
# time.sleep(999)

# Apply the filters and sort
filter_2_year_lows()
sort_by_price()

#time.sleep(999)

# time.sleep(1)
# Add the first N sales to the cart
for i in range(1, (num_sales_to_add + 1)):
    add_to_cart(i)

    # Opens a new tab and switches to new tab
driver.switch_to.new_window('tab')

driver.get("https://store.steampowered.com/cart/")

time.sleep(999)
# Close the browser
# driver.quit
