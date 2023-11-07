import concurrent.futures
from datetime import datetime

import pandas as pd
from helpers import get_days_month, get_pages_links
from shared_globals import base_urls_pages

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

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_pages_links, base_urls_list)

contenido = dict()
contenido["url_base"] = base_urls_pages
today = datetime.today().strftime("%Y-%m-%d")

print(len(base_urls_pages))
df = pd.DataFrame(contenido)
df.to_csv(f"scraped-link-{year}-{month}-at-{today}.csv", index=False)
print("Complete.")
