import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pathlib import Path

# fetch admin credentials to send email
load_dotenv(dotenv_path=Path(__file__).parents[2] / "credentials.env")
sender = os.getenv("EMAIL")
password = os.getenv("EMAIL_PW")

def alert(alert_type, recipient, product, old_price=None, new_price=None):
    # check the product's change type to determine email message
    if alert_type == "price_rise":
        subject = "Alert! Product Price Raised"
        body = (f"Hello!\n\nThe price of: '{product}' "
                f"has increased from RM{old_price:.2f} to RM{new_price:.2f}."
                f"\n\n- PriceWatch")
    elif alert_type == "price_drop":
        subject = "Alert! Product Price Dropped"
        body = (f"Hello!\n\nThe price of: '{product}' "
                f"has decreased from RM{old_price:.2f} to RM{new_price:.2f}."
                f"\n\n- PriceWatch")
    elif alert_type == "unavailable":
        subject = "Alert! Product Out Of Stock"
        body = (f"Hello!\n\nThe product: '{product}' is currently out of stock."
                f"\n\n- PriceWatch")
    elif alert_type == "available":
        subject = "Alert! Product Back In Stock"
        body = (f"Hello!\n\nThe product: '{product}' is now back in stock, "
                f"at a price of RM{new_price:.2f}."
                f"\n\n- PriceWatch")
    else:
        return

    # message element variables
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # connect & login to gmail server to send message
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(msg["From"], password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())