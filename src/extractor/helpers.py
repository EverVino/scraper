from datetime import date, timedelta, datetime
from calendar import monthrange
from shared_globals import *
import requests
from bs4 import BeautifulSoup

def get_days_month(year, month):
    nb_days = monthrange(year, month)[1]

    return [f"{year}/{month}/{day}" for day in range(1, nb_days+1)]

def listing_dates(begin_date, end_date):
    days = [begin_date + timedelta(days=x) for x in range((end_date - begin_date).days+1)]

    return days

def get_pages_links(start_url):
    response = requests.get(start_url)
    print(start_url, response.status_code)
    if response.status_code != 200:
        print(f"Error in url {start_url}")
        return
    try:
        soup = BeautifulSoup(response.content, features="html.parser")
        base_urls_pages.append(start_url)
        page_info = soup.body.find("span", class_="page_info").text
        page = int(page_info.split()[-1])
        for i in range(2, page+1):
            url = start_url + "/page/" + str(i)
            base_urls_pages.append(url)
    except:
        print(f"Error in url {start_url}")
        return
    return

def get_articles_links_day(url_base):
    response = requests.get(url_base)
    
    if response.status_code != 200:
        print(f"Error in url {url_base}")
        return False
        
    contenido = dict()
    contenido["url_base"] = []
    contenido["download_date"] = []
    contenido["title"] = []
    contenido["url"] = []
    contenido["fecha"] = []
    
    date = url_base[-10:]
    
    base_soup = BeautifulSoup(response.content, features="html.parser")
    pages_link = get_pages_links(url_base, base_soup)
    
    for url in pages_link:
        page_response = requests.get(url)
        if page_response.status_code != 200:
            print(f"Error in the url {url}")
            continue
        soup = BeautifulSoup(page_response.content, features="html.parser")
        
        extract_links(url, url_base, date, soup, contenido)

    df = pd.DataFrame(contenido)
    df.to_csv("2023-10-04.csv")

    return contenido["url"]
