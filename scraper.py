# import pyinputplus as pyip
import requests
from bs4 import BeautifulSoup
import emailer
from time import sleep

URL = "https://www.apple.com/shop/refurbished/mac/macbook-air"
MINUTES_TO_SLEEP = 20

def scrape_apple_refurb_webpage():
    """
    Scrape Apple refurb website to find M2 Macbook Air deals.
    """
    counter = 0
    while(True):
        response = requests.get("https://www.apple.com/shop/refurbished/mac/2020-macbook-air")
        soup = BeautifulSoup(response.content, 'html.parser')

        all_devices = soup.find("div", class_="rf-refurb-category-grid-no-js").ul
        content = []
        if "MacBook Air Apple M2" in str(all_devices):
            for device in all_devices.find_all("li"):
                if "MacBook Air Apple M2" in device.h3.a.text:
                    content.append(device)
            print("GOING TO EMAILER")
            emailer.send_email(content)
            break
        else:
            # sleep for MINUTES_TO_SLEEP minutes if couldn't find M2 Macbook Air
            print("SLEEPING", counter)
            counter += 1
            sleep(60 * MINUTES_TO_SLEEP)

    # <div class="rf-refurb-category-grid-no-js">

if __name__ == '__main__':
    scrape_apple_refurb_webpage()
