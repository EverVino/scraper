import random
from calendar import monthrange
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from shared_globals import (
    article_date,
    article_link,
    article_title,
    bad_description,
    bad_url_base,
    base_urls_pages,
    url_base_page,
    wrong_urls_pages,
)

with open("proxies.txt", "r") as file:
    proxies = file.read().splitlines()


def get_date_from_url(s):
    splited = s.split("/")
    if splited[-2] != "page":
        return splited[-3] + "/" + splited[-2] + "/" + splited[-1]
    else:
        return splited[-5] + "/" + splited[-4] + "/" + splited[-3]


def get_days_month(year, month):
    nb_days = monthrange(year, month)[1]

    return [f"{year}/{month}/{day}" for day in range(1, nb_days + 1)]


def listing_dates(begin_date, end_date):
    days = [
        begin_date + timedelta(days=x) for x in range((end_date - begin_date).days + 1)
    ]

    return days


def extract_links(url_base, date, soup):
    try:
        container = soup.body.find("div", class_="jeg_block_container")
        block_articles = container.find_all(
            "article", class_="jeg_post jeg_pl_md_2 format-standard"
        )

        for article in block_articles:
            title = article.find("h3", class_="jeg_post_title")
            url = title.a["href"]

            if "PUBLICA TU AVISO" not in title.text:
                print(title.text)
                article_link.append(url)
                url_base_page.append(url_base)
                article_title.append(title.text)
                article_date.append(date)

    except Exception as e:
        print(e, url_base)
        bad_url_base.append(url_base)
        bad_description.append("Error in extracting links")

    return


def get_pages_links(start_url):
    """
    Get base links from base url
    """
    proxie = random.choice(proxies)
    response = requests.get(start_url, proxies={"http": f"http://{proxie}"}, timeout=20)
    print(start_url, response.status_code)

    if response.status_code != 200:
        print(f"Error in url {start_url}")
        return
    try:
        soup = BeautifulSoup(response.content, features="html.parser")
        base_urls_pages.append(start_url)
        page_info = soup.body.find("span", class_="page_info").text
        page = int(page_info.split()[-1])
        for i in range(2, page + 1):
            url = start_url + "/page/" + str(i)
            base_urls_pages.append(url)
    except Exception as e:
        print(e)
        print(f"Error in url {start_url}")
        wrong_urls_pages.append(url)

    return


def get_articles_links_day(url_base):
    proxie = random.choice(proxies)
    response = requests.get(url_base, proxies={"http": f"http://{proxie}"}, timeout=20)
    print(url_base, response.status_code)

    if response.status_code != 200:
        print(f"Error in url {url_base}")
        bad_url_base.append(url_base)
        bad_description.append("wrong status_code")
        return

    date = get_date_from_url(url_base)

    try:
        soup = BeautifulSoup(response.content, features="html.parser")
        extract_links(url_base, date, soup)

    except Exception as e:
        print(url_base, e)
        bad_url_base.append(url_base)
        bad_description.append("Exception using BS4")

    return
