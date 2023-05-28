import openai
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from serpapi import GoogleSearch

import amazon_scraper

openai.api_key = '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'
LLM_MODEL = "gpt-4"
AMAZON_ID = "diptobiswas-20"

def get_camping_itemlist(requirement):
    # Define the conversation messages
    messages = [
        {"role": "user", "content": "Act as a professional camping equipment seller. You need to provide a list of 5 camping items based on the user requirements."},
        {"role": "user", "content": f"The user requirements are: {requirement}"},
        {"role": "user", "content": "The only output should be only a list formatted by: ['item1', 'item2', 'item3', 'item4', 'item5']"},
    ]

    # Make a request to the chat models
    response = openai.ChatCompletion.create(
      model=LLM_MODEL,
      messages=messages,
      temperature=0.2,
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # The reply should be a list of PC parts
    return assistant_reply

def create_budget(requirement, budget, items):

    # Define the conversation messages
    messages = [
        {"role": "user", "content": "You are an expert accountant. Depending on the user requirements you need to allocate the budget fully."},
        {"role": "user", "content": f"I need a budget allocated for each {items} for my requirements: {requirement}. My budget is {budget}."},
        {"role": "user", "content": "The only output should be only a JSON formatted as: {'item_name': 'budget'}"},
    ]

    # Make a request to the chat models
    response = openai.ChatCompletion.create(
      model=LLM_MODEL,
      messages=messages,
      temperature=0.2,
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # The reply should be a list of PC parts
    return assistant_reply

def create_affiliate_link(url, associate_id):
    # Parse the url
    parsed_url = urlparse(url)
    
    # Get the query params from the url
    query_params = parse_qs(parsed_url.query)
    
    # Add additional parameters
    query_params.update({
        "linkCode": "ll1", 
        "tag": associate_id,
        "linkId": "971b0f63461afc58b04edb4ef21d4fe5",
        "language": "en_CA",
        "ref_": "as_li_ss_tl"
    })
    
    # Create new url with updated query params
    new_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
    
    return urlunparse(new_url)

def get_youtube_link(product_name):
  params = {
  "engine": "youtube",
  "search_query": {product_name + " review"},
  "api_key": "3cf4fdc5603a1fef0a8e121bcd6b9d28fd422dc3fc187c469958a406e9b5dfa4"
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  video_results = results["video_results"]

  return video_results[0]["link"]

# url = "https://www.amazon.ca/Intex-Seahawk-4-Person-Inflatable-Aluminum/dp/B00177BQC6/ref=sr_1_7?keywords=boat&qid=1685224355&sr=8-7"
# associate_id = "diptobiswas-20"
# print(create_affiliate_link(url, associate_id))

# print(get_youtube_link("Intex-Seahawk-4-Person"))

# requirement = "I am going to muskoka, the weather will be sunny. I already have a tent and cooler."
# budget = "$1000"

# items = json.loads(get_camping_itemlist(requirement).replace("'", "\""))
# budget = create_budget(requirement, budget, items)

# budget = {
#     "Sleeping Bag": 250,
#     "Camping Stove": 250,
#     "Sunscreen": 150,
#     "Insect Repellent": 150,
#     "Camping Chair": 200
#   }

# amazon_links = [
#     {
#         "item_type": "boat",
#         "name": "Intex-Seahawk-4-Person-Inflatable-Aluminum",
#         "link": "https://www.amazon.ca/Intex-Seahawk-4-Person-Inflatable-Aluminum/dp/B00177BQC6/ref=sr_1_7?keywords=boat&qid=1685224355&sr=8-7",
#         "price": 100,
#     }
# ]

# purchase_list = [
#       {
#         "item_type": "boat",
#         "item_name": "Intex-Seahawk-4-Person-Inflatable-Aluminum",
#         "price": "$100",
#         "amazon-link": "https://www.amazon.ca/Intex-Seahawk-4-Person-Inflatable-Aluminum/dp/B00177BQC6/ref=sr_1_7?keywords=boat&qid=1685224355&sr=8-7",
#         "youtube-link": "https://www.youtube.com/watch?v=NjhCIcplw3Q"
#       }
# ]
def get_amazon_links(budget):
    product_info_dict = []

    for product, price in budget.items():
        info = amazon_scraper.get_product_information(product, price)
        product_info_dict.append(info)

    return product_info_dict
        

def create_purchase_list(amazon_links):
    purchase_list = []

    for amazon_link in amazon_links:
        purchase_item = {
            "item_type": amazon_link["item_type"],
            "item_name": amazon_link["name"],
            "price": amazon_link["price"],
            "amazon-link": create_affiliate_link(amazon_link["link"], AMAZON_ID),
            "youtube-link": {(get_youtube_link(amazon_link["name"] + " review"))}
        }
        purchase_list.append(purchase_item)

    return purchase_list

# print(type(budget))
# amazon_links = get_amazon_links(json.loads(budget))
# print(amazon_links)

# print(create_purchase_list(amazon_links))


