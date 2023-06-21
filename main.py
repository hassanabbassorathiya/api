from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import json
app = FastAPI()

@app.get('/main')
def index():
    return {'I am':'alive'}


@app.get('/')
def property(start_page_no: int, end_page_number: int):
     headers = {
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
     }
     # Get page Url
     properties = []
     for page_no in range(start_page_no,end_page_number+1):
          item_count = 0
          url = (f'https://www.propertyfinder.ae/en/search?c=1&page={page_no}')
          print(f'page number: {page_no}')
          response = requests.get(url, headers=headers)
          print(response)
          soup = BeautifulSoup(response.content, 'html.parser')

          card_item  = soup.find_all("div", class_='card-list__item')
          # properties = []
          for card_link in card_item:

               card_url = 'https://www.propertyfinder.ae'+card_link.a['href'] # Particular Product Link
               item_count = item_count+1
               print(item_count)
               img_url = card_link.find('img').get('src')
               amenities = []
               responses = requests.get(card_url, headers=headers)
               main_soup = BeautifulSoup(responses.content, 'html.parser')

               property_page = main_soup.find_all("div", class_="property-page__column--left")

               for itemScrap in property_page:
                    try:
                         Property_type = itemScrap.find("div",class_="property-facts__value").text.strip()
                    except AttributeError:
                         Property_type = None
                    try:
                         price = itemScrap.find('div', class_='property-price__price').text.strip()
                    except AttributeError:
                         price = None
                    try:
                         location = itemScrap.find('div',class_='text text--size3').text.strip()
                    except AttributeError:
                         location = None
                    for k in range(0,15):
                         for j in itemScrap.find_all("div")[k]:
                              if j.get_text(strip=True) == 'Bedrooms:':
                                   broom = itemScrap.find_all("div")[k+1]
                                   bedroom = broom.get_text(strip=True)
                                   break
                    for k in range(0,15):
                         for j in itemScrap.find_all("div")[k]:
                              if j.get_text(strip=True) == 'Bathrooms:':
                                   broom = itemScrap.find_all("div")[k+1]
                                   bathroom = broom.get_text(strip=True)
                                   break
                    try:
                         area = itemScrap.find('span',class_='property-facts__text').text.strip()
                    except AttributeError:
                         area = None
                    for det in itemScrap.find_all("div", class_='property-amenities__list'):
                         amenities.append(det.get_text(strip=True))
                    try:
                         agent_name = itemScrap.find('a',class_='text text--size3 link link--underline property-agent__name').text.strip()
                    except AttributeError:
                         agent_name = 'none'
                    products = {
                         'Property type':Property_type,
                         'price':price,
                         'location':location,
                         'bedroom':bedroom,
                         'bathroom':bathroom,
                         'area':area,
                         'amenities':amenities,
                         'img url': img_url,
                         'agent name': agent_name
                    }
                    properties.append(products)
                    amenities = []
                    file_path = "Z:/PropertyFinder/properties.json"
          # saveProperties.append(properties)
                    with open(file_path, 'w') as f:
                         json.dump(properties, f, indent=4)

                    with open('properties.json', 'r') as f:
                         property = json.load(f)
     return properties