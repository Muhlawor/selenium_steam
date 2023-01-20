import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc

opts = ChromeOptions()
opts.add_argument("--window-size=1400,1000")
opts.add_argument("--user-data-dir=C:\\Users\\ASUS_TUF_DASH_F15\\AppData\\Local\\Google_2\\Chrome\\User Data")
opts.add_argument('--profile-directory=Profile 69')

driver = uc.Chrome(options=opts)

# Navigate to the website
driver.get("https://steamdb.info/sales/?cc=ar&min_reviews=0&min_rating=0&min_discount=0&category=29")


# Function to filter the sales by 2 year lows
def filter_2_year_lows():
    filter_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/form/div/div[4]/div[3]/div")))
    filter_button.click()


# Function to sort the sales by price
def sort_by_price():
    sort_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/table/thead/tr/th[5]")))
    sort_button.click()


# Function to add a specific sale to the cart
def add_to_cart(sale_index):
    sale_link = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,
                                                                                                 f"/html/body/div["
                                                                                                 f"5]/div[1]/div["
                                                                                                 f"2]/div[2]/div["
                                                                                                 f"2]/div[2]/div/div["
                                                                                                 f"2]/table/tbody/tr["
                                                                                                 f"{sale_index}]/td["
                                                                                                 f"1]/a")))
    sale_link.click()
    driver.switch_to.window(driver.window_handles[1])
    try:
        add_to_cart_button = WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "Add to Cart")))
        if add_to_cart_button.text == "In Cart":
            print("Already in Cart")
            return
        add_to_cart_button.click()
    except TimeoutException:
        print("Already in Cart")
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


num_sales_to_add = 1



# Apply the filters and sort
filter_2_year_lows()
sort_by_price()

#time.sleep(999)

time.sleep(1)
# Add the first N sales to the cart
for i in range(1, (num_sales_to_add + 1)):
    add_to_cart(i)

    # Opens a new tab and switches to new tab
driver.switch_to.new_window('tab')

driver.get("https://store.steampowered.com/cart/")

time.sleep(999)
# Close the browser
# driver.quit
