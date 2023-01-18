import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
from selenium import webdriver

opts = ChromeOptions()
opts.add_argument("--window-size=1400,1000")

opts.add_argument("--user-data-dir=C:\\Users\\ASUS_TUF_DASH_F15\\AppData\\Local\\Google_2\\Chrome\\User Data")
opts.add_argument('--profile-directory=Profile 69')

driver = uc.Chrome(options=opts)

driver.get("https://steamdb.info/sales/?cc=ar&min_reviews=0&min_rating=0&min_discount=0&category=29")
time.sleep(5)
#driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/form/div/div[4]/div[1]/div").click()
#driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/form/div/div[4]/div[2]/div").click()
# show 2 year lows
driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/form/div/div[4]/div[3]/div").click()
# sorting by price
driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/table/thead/tr/th[5]").click()

time.sleep(6000)
