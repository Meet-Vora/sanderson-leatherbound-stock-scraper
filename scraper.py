# import pyinputplus as pyip
import requests
from bs4 import BeautifulSoup
import emailer
from time import sleep

BASE_URL = 'https://www.dragonsteelbooks.com'
LEATHERBOUND_BOOKS_SLUG = "/collections/leatherbound-books"
BOOKS_TO_ALERT_FOR = ['The Way of Kings Leatherbound Book', 'Mistborn Leatherbound Book', 'Words of Radiance Leatherbound Book', 'Oathbringer Leatherbound Book']
EXECUTION_INTERVAL_IN_MINUTES = 30

def scrape_leatherbound_books():
    counter = 0
    while(True):
        response = requests.get(BASE_URL + LEATHERBOUND_BOOKS_SLUG)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_leatherbounds = soup.find("div", class_="collection-products").div.contents[3].find("div", class_='o-layout').contents
        all_leatherbounds = [book for book in all_leatherbounds if book != '\n']

        data = []
        report_in_stock = False
        for book in all_leatherbounds:
            book_info = {
                'title': book.div.find('div', class_='product-card__details').a.text.strip(), 
                'link': BASE_URL + book.div.find('div', class_='product-card__details').a['href'],
                'price': book.div.find('span', class_='money').text,
                'in_stock': book.select("[class*=product-card__label]") == []
            }
            data.append(book_info)
            if book_info['title'] in BOOKS_TO_ALERT_FOR and book_info['in_stock']:
                report_in_stock = True

        if report_in_stock:
            emailer.send_email(data)
        else:
            # sleep for EXECUTION_INTERVAL_IN_MINUTES minutes if not in stock
            print("SLEEPING #", counter)
            counter += 1
            sleep(60 * EXECUTION_INTERVAL_IN_MINUTES)

        print(data)

if __name__ == '__main__':
    scrape_leatherbound_books()
