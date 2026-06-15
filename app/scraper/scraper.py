from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def scrape_price(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-buster-extension")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # test selenium by accessing the target service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    WebDriverWait(driver, 7)

    # find element containing the price, then scrape & format data
    price = driver.find_element(By.CSS_SELECTOR, "span.pdp-v2-product-price-content-salePrice-amount")
    print(price.text)

    driver.quit()
scrape_price("https://www.lazada.com.my/products/pdp-i2070565192-s11757680082.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Aheadphones%253Bnid%253A2070565192%253Bsrc%253ALazadaMainSrp%253Brn%253Aedf404dfb18a3f8d67e7a6b551cc536a%253Bregion%253Amy%253Bsku%253A2070565192_MY%253Bprice%253A25.5%253Bclient%253Adesktop%253Bsupplier_id%253A300146649170%253Bsession_id%253A%253Bbiz_source%253Ah5_internal%253Bslot%253A27%253Butlog_bucket_id%253A470687%253Basc_category_id%253A156%253Bitem_id%253A2070565192%253Bsku_id%253A11757680082%253Bshop_id%253A1427559%253BtemplateInfo%253A107880_E%2523-1_A3_C%2523&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=Wp%20Kuala%20Lumpur&price=25.5&priceCompare=skuId%3A11757680082%3Bsource%3Alazada-search-voucher%3Bsn%3Aedf404dfb18a3f8d67e7a6b551cc536a%3BoriginPrice%3A2550%3BdisplayPrice%3A2550%3BisGray%3Afalse%3BsinglePromotionId%3A-1%3BsingleToolCode%3AmockedSalePrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1781496576073&ratingscore=4.824247355573637&request_id=edf404dfb18a3f8d67e7a6b551cc536a&review=1229&sale=4002&search=1&source=search&spm=a2o4k.searchlist.list.27&stock=1")