from apscheduler.schedulers.blocking import BlockingScheduler
from app.scraper.scraper import scrape_price
from app.database.database import get_history, insert_history, insert_product
from app.alerts.alerts import alert

# configure scheduling instance
sch = BlockingScheduler()

# call the function for each time interval specified
@sch.scheduled_job("interval",  hours=24)
def check_price(old_price, new_price):
    old = get_history(old_price)
    new = scrape_price(new_price)

sch.start()