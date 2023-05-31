from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from decimal import Decimal
from pprint import pprint


def filterAdLinks(product):
  link = product.find(
    'a', {
      'class':
      'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
    })['href']

  regex_pattern = r"^(?!\/gp\/).*"

  return re.match(regex_pattern, link)


def get_products_from_amazon(product_type):

  # chrome_options = Options()
  # chrome_options.add_argument("--headless")

  # Create a new instance of the Firefox driver
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  # driver = webdriver.Chrome(options=chrome_options)

  # Navigate to the Amazon website
  driver.get(f'http://www.amazon.ca/s?k={product_type}')

  # Wait for the page to load
  time.sleep(2)

  # Parse the page source with BeautifulSoup
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  # Find all products
  products = soup.find_all(
    'div', {
      'class':
      'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'
    })

  products = list(filter(filterAdLinks, products))

  products_json_list = []

  for product in products:
    try:
      product_a_tag = product.find(
        'a', {
          'class':
          'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
        })
      price_span_tag = product.find('span', 'a-price')

      link = 'https://www.amazon.ca' + product_a_tag['href']

      name = product_a_tag.get_text().replace('\u2013', '-')
      price_str = price_span_tag.find('span', 'a-offscreen').get_text()[1:]

      # star_rating_span = product.find(
      #     'span', {'class': 'a-icon-alt'}
      # ).get_text().split(" ")

      # total_ratings_span = product.find(
      #     'span', {'class': 'a-size-base s-underline-text'}).get_text().strip()

      # total_ratings = int(
      #     Decimal(re.sub(r'[^\d.]', '', total_ratings_span)))

      # star_rating = float(star_rating_span[0].strip())

      # print(star_rating, total_ratings)
      price = float(Decimal(re.sub(r'[^\d.]', '', price_str)))

      products_json_list.append({
        'item_type': product_type,
        'name': name,
        'link': link,
        'price': price,
        # 'stars': star_rating,
        # 'total_reviews': total_ratings
      })

    except (TypeError, AttributeError):
      # print('error')
      continue

  driver.quit()

  return products_json_list


def get_product_information(product_type, price):
    products = get_products_from_amazon(product_type)

    # Filter by price
    price_filtered_products = []

    for product in products:
        if (product["price"] <= price):
            price_filtered_products.append(product)

    # stars_filtered_products = [
    #     p for p in price_filtered_products if p['stars'] >= 4.5]

    # reviews_filtered_products = [
    #     p for p in stars_filtered_products if p['total_reviews'] >= 10]

    # pprint(price_filtered_products)
    if price_filtered_products == []:
        return None
    else:
        return price_filtered_products[0]


# if __name__ == "__main__":
#   product_type = 'boat'
#   price_limit = 50

#   result = get_product_information(product_type, price_limit)

#   pprint(result)
