from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from geopy.geocoders import Nominatim



options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
geolocator = Nominatim(user_agent="michelin_scraper")


def gather_links():
    restaurant_links = []
    flag = "ile-de-france/paris/restaurant/"
    page = 1
    with open("Webscrapping\Restaurant_Links.txt", "w") as file:
        file.seek(0)
        file.truncate()
        while True:
            url = f"https://guide.michelin.com/en/fr/ile-de-france/paris/restaurants/page/{page}?sort=distance"
            try:
                request = requests.get(url, timeout= 10)
                if request.status_code != 200: 
                    print("No more pages to be found")
                    break

                mm_soup = BeautifulSoup(request.text, 'lxml')
                found_links = 0
                for link in mm_soup.find_all('a', class_ = "link"):
                    href = link.get("href")
                    if flag in href:
                        full_link = f"https://guide.michelin.com{href}"
                        restaurant_links.append(full_link)
                        file.write(full_link + "\n")
                        found_links += 1
                print(f"Page {page}: {found_links} restaurants added")
            except requests.exceptions.RequestException as e:
                    print(f"[ERROR] Failed to fetch page {page}: {e}")
                    break  # Stop on network errors
            
            page += 1
            time.sleep(0.5)
    # print(restaurant_links)
    return restaurant_links

def gather_data(url):
     #url; name; price; cuisine; coordinates; address; hours(if they have); website href
    driver.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, "lxml")
    print(f"Connected to {url}")
    name = soup.find("h1", class_ = "data-sheet__title").text
    
    address_soup = soup.find("div", class_ = "data-sheet__block--text")
    address = address_soup.text.strip()
    latitude, longitude = get_coordinates(address)      
    
    p_c_line = address_soup.find_next().text.strip()
    price = " ".join(p_c_line[:4].split())
    cuisine = " ".join(p_c_line[-20:].split())
    website_soup = soup.find("a", class_="btn btn-sm btn-black-border btn-round filter-icon arrow-up d-flex js-dtm-link")
    if website_soup == None:
         website = "NONE"
    else:
        website = website_soup.get("href")

    
    return f"{name}; {price}; {cuisine}; {latitude}, {longitude}; {address}; {website}\n"

def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return "N/A", "N/A"
    except Exception as e:
        print(f"Geocoding error: {e}")
        return "N/A", "N/A"

def get_hours(soup):
    hours = soup.find_all("div", class_ = "card--content")
    if  hours == []: return "Not Listed"

    ret = ""
    DAY = ['M', 'T', 'W', 'H', 'F', 'S', 'D']
    for i in range(7):
        
        ret += f"{DAY[i]: }"

links = []
file =  open("Webscrapping\Restaurant_Links.txt", "r")
for line in file:
    links.append(line)
file.close()
i = 1
with open("Webscrapping\Restaurant_Info.txt", "w", encoding='utf-8' ) as target:
    for link in links:
        data = gather_data(link)
        target.write(data)
        print(f"Entry {i}: {data}")
        i += 1
target.close()


# gather_links()
# gather_data("https://guide.michelin.com/en/ile-de-france/paris/restaurant/la-table-de-mee")
# gather_data("https://guide.michelin.com/en/ile-de-france/paris/restaurant/la-mediterranee")


