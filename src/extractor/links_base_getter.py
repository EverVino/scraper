from helpers import (
    listing_dates,
    get_pages_links,
    get_articles_links_day,
    get_days_month,
)

import concurrent.futures
import pandas as pd
from shared_globals import *
# Get the list dates
# lets do by month
# Implement to scrape the whole year just do that 
# when you use different ip proxies
# do more research
# for month in range(1,13):
#     month_days = get_days_month(year, month)

year = 2023
month = 10
months_days = get_days_month(year, month)

base_url = "https://www.eldiario.net/portal/"

base_urls_list = [base_url + day for day in months_days]

print(len(base_urls_list))
links = []

# TODO: seems that the page is not working
# I get blocked by ip so we need to use 
# ip rotating or somethins like that
get_pages_links(base_urls_list[2])
# for url in base_urls_list:
#     get_pages_links(url)
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(get_pages_links, base_urls_list)

print(len(base_urls_pages))
df = pd.DataFrame(base_urls_pages)
df.to_csv('concurrent-urls.csv', index=False)
print('Complete.')
