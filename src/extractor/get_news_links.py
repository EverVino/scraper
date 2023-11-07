import concurrent.futures
from datetime import datetime

import pandas as pd
from helpers import get_articles_links_day
from shared_globals import (article_date, article_link, article_title,
                            bad_description, bad_url_base, base_urls_pages,
                            url_base_page)

# This is just for the name
year = 2023
month = 10

# select the source to extract new links
df = pd.read_csv("scraped-link-2023-10-at-2023-11-07.csv")

base_links = list(df["url_base"])
print(len(base_links))

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_articles_links_day, base_links)

print(len(base_urls_pages))
content = dict()
content["base_page"] = url_base_page
content["article_date"] = article_date
content["article_title"] = article_title
content["article_url"] = article_link

wrong_base_url = dict()
wrong_base_url["wrong_url"] = bad_url_base
wrong_base_url["description"] = bad_description

today = datetime.today().strftime("%Y-%m-%d")

dflink = pd.DataFrame(content)
dflink.to_csv(f"news-links-{year}-{month}-at-{today}.csv", index=False)

dfwrong = pd.DataFrame(wrong_base_url)
dfwrong.to_csv(f"wrong-news-links-{year}-{month}-at-{today}.csv", index=False)
print("Complete.")
