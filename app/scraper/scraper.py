from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def scrape(url):
    # test selenium by accessing the target service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    WebDriverWait(driver, 5)

    # find element containing product info, then scrape & format data
    price = driver.find_element(By.CSS_SELECTOR, "span.pdp-v2-product-price-content-salePrice-amount")
    name = driver.find_element(By.CSS_SELECTOR, "h1.pdp-mod-product-badge-title-v2")
    stock = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='off'][type='text']")
    product = {
        "name": name.text,
        "price": float(price.text),
        "stock": int(stock.get_attribute("max"))
    }

    # close service and return product data after scraping is done
    driver.quit()
    return product

target = scrape("https://www.lazada.com.my/products/gaming-headphone-noise-cancelling-headset-wired-overear-earphone-call-center-headset-with-microphone-i2070565192-s11757680082.html?")
print(target)