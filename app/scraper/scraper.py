import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# test if selenium is working, then scrape and format data
def scrape_price(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(10)
    price = driver.find_element(By.CSS_SELECTOR, "div.IZPeQz.B67UQ0")
    print(price.text)
    driver.quit()
scrape_price("https://shopee.com.my/P9-Wireless-Bluetooth-Sports-Headphones-with-Mic-Noise-Reduction-On-Ear-Stereo-Headset-i.1206023866.24878743362?extraParams=%7B%22display_model_id%22%3A176458449017%2C%22model_selection_logic%22%3A3%7D")