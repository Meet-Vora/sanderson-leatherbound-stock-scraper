# import pyinputplus as pyip
import requests
from bs4 import BeautifulSoup
# import emailer
from lxml import etree
from time import sleep

BASE_URL = 'https://www.dragonsteelbooks.com'
LEATHERBOUND_BOOKS_SLUG = "/collections/leatherbound-books"
# LEATHERBOUND_ELEMENTS_CONTAINER_XPATH = '/html/body/div[3]/div[4]/div[2]/section/div/div/div/div[2]/div/div[2]/div[2]'
LEATHERBOUND_ELEMENTS_CONTAINER_XPATH = '//*[@id="collection-main"]/div[2]/div/div[2]/div[2]'
BOOKS_TO_ALERT_FOR = ['The Way of Kings Leatherbound Book', 'Mistborn Leatherbound Book']
EXECUTION_INTERVAL_IN_MINUTES = 20

def scrape_leatherbound_books():
    counter = 0
    report_in_stock = False
    while(not report_in_stock):
    # while(True):
        response = requests.get(BASE_URL + LEATHERBOUND_BOOKS_SLUG)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_leatherbounds = soup.find("div", class_="collection-products").div.contents[3].find("div", class_='o-layout').contents
        all_leatherbounds = [book for book in all_leatherbounds if book != '\n']

        data = []
        for book in all_leatherbounds[3:4]:
            book_info = {
                'title': book.div.find('div', class_='product-card__details').a.text.strip(), 
                'link': BASE_URL + book.div.find('div', class_='product-card__details').a['href'],
                'price': book.div.find('span', class_='money').text,
                'in_stock': book.select("[class*=product-card__label]") is None
                # 'price': book.div.find('div', class_='product-card__details').div.a.p.span.span.text
            }
            print(book.select("[class*=product-card__label]"))
            data.append(book_info)
            # if title in BOOKS_TO_ALERT_FOR:
                # if is_in_stock
            report_in_stock = True
        print(data)
            
        # content = []
        # if "MacBook Air Apple M2" in str(all_devices):
        #     for device in all_devices.find_all("li"):
        #         if "MacBook Air Apple M2" in device.h3.a.text:
        #             content.append(device)
        #     print("GOING TO EMAILER")
        #     emailer.send_email(content)
        #     break

        # else:
        #     # sleep for MINUTES_TO_SLEEP minutes if couldn't find M2 Macbook Air
        #     print("SLEEPING", counter)
        #     counter += 1
        #     sleep(60 * MINUTES_TO_SLEEP)
        break

    # <div class="rf-refurb-category-grid-no-js">

if __name__ == '__main__':
    scrape_leatherbound_books()
