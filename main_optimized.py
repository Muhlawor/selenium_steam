import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc

opts = ChromeOptions()
opts.add_argument("--window-size=1800,1400")
opts.add_argument("--user-data-dir=C:\\Users\\vasya\\AppData\\Local\\Google_2\\Chrome\\User Data")
opts.add_argument('--profile-directory=Profile 69')

driver = uc.Chrome(options=opts)

driver.get("https://steamdb.info/sales/?cc=ar&min_reviews=0&min_rating=0&min_discount=0&category=29")


def filter_2_year_lows():
    filter_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#js-discounts-minor > div")))
    filter_button.click()


def sort_by_price():
    sort_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#DataTables_Table_0 > thead > tr > th:nth-child(5)")))
    sort_button.click()


def add_to_cart(sale_index, max_price):
    sale_price_selector = f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(5)"
    sale_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sale_price_selector)))
    sale_price = float(sale_price_element.text.replace("ARS$ ", "").replace(',', '.'))

    if sale_price >= max_price:
        print(f"Sale {sale_index} is above the price threshold, skipping...")
        return

    sale_link_selector = f"#DataTables_Table_0 > tbody > tr:nth-child({sale_index}) > td:nth-child(1) > a"
    sale_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sale_link_selector)))
    sale_link.click()
    driver.switch_to.window(driver.window_handles[1])

    try:
        add_to_cart_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[id^='btn_add_to_cart_'] > span")))
        if "In Cart" in add_to_cart_button.get_attribute("innerHTML"):
            print(f"Sale {sale_index} is already in the cart")
        else:
            add_to_cart_button.click()
            WebDriverWait(driver, 1).until(EC.url_matches("https://store.steampowered.com/cart/"))
    except TimeoutException:
        print(f"Sale {sale_index} is already in the cart or not available")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


num_sales_to_add = 50
max_price = 50

filter_2_year_lows()
sort_by_price()

for i in range(1, num_sales_to_add + 1):
    add_to_cart(i, max_price)

driver.switch_to.new_window('tab')
driver.get("https://store.steampowered.com/cart/")
time.sleep(999)

# Close the browser
# driver.quit()
