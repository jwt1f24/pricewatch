from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from app.scraper.scraper import scrape
from app.database.database import get_products, insert_history, update_product
from app.alerts.alerts import alert

# configure scheduling instance
sch = BlockingScheduler()

# call the function for each time interval specified
@sch.scheduled_job("interval",  hours=24)
def check_price():
    products = get_products()
    for product in products:
        old_price = product["current_price"]
        new = scrape(url=product["url"])

        # compare both prices, replace old price if new price is different
        if old_price != new["price"] or product["stock"] != new["stock"]:
            update_product(product["product_id"], new["price"], new["stock"])
            insert_history(product["product_id"], new["price"], datetime.now())

            # price condition
            if new["price"] > old_price:
                alert("price_rise", product["email"], product["name"], old_price, new["price"])
            elif new["price"] < old_price:
                alert("price_drop", product["email"], product["name"], old_price, new["price"])

            # stock condition
            if product["stock"] > 0 and new["stock"] <= 0:
                alert("unavailable", product["email"], product["name"], old_price, new["price"])
            elif product["stock"] <= 0 and new["stock"] > 0:
                alert("available", product["email"], product["name"], old_price, new["price"])
        else:
            continue

# sch.start()