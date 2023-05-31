import pprint
import amazon_scraper

def get_amazon_links(budget):
    product_info_dict = []

    for product, price in budget.items():
        info = amazon_scraper.get_product_information(product, price)
        product_info_dict.append(info)

    return product_info_dict

import concurrent.futures

def get_amazon_links_concurrency(budget):
    product_info_dict = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(amazon_scraper.get_product_information, product, price) for product, price in budget.items()]

    for future in concurrent.futures.as_completed(futures):
        try:
            info = future.result()
            product_info_dict.append(info)
        except Exception as e:
            print("Exception occurred: ", e)
            
    return product_info_dict


budget = {
    "Sleeping Bag": 250,
    "Camping Stove": 250,
    "Sunscreen": 150,
    "Insect Repellent": 150,
    "Camping Chair": 200
  }

amazon_links = get_amazon_links_concurrency(budget)

print(amazon_links)