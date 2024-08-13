import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_page(driver, url):
    driver.get(url)
    time.sleep(2)  
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'w3-table w3-bordered'})

    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:
            cols = [col.text.strip() for col in row.find_all('td')]
            rows.append(cols)
        return headers, rows
    else:
        return None, None

def scrape_all_pages(driver, url):
    all_data = []
    page_number = 1
    while True:
        current_url = f"{url}&page={page_number}" if page_number > 1 else url
        print(f"Scraping {current_url}...")
        headers, rows = scrape_page(driver, current_url)
        if rows:
            if not all_data:
                all_data.append(headers)  
            all_data.extend(rows)
            page_number += 1
        else:
            break
    return all_data

chrome_options = Options()
chrome_options.add_argument("--headless")  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_file = 'constituencies.csv'
data = pd.read_csv(csv_file)

for _, row in data.iterrows():
    state_name = row['State Name']
    state_id = row['State ID']
    constituency = row['Constituency']
    link = row['Constituency Link']
    
    state_dir = f"./{state_name}"
    os.makedirs(state_dir, exist_ok=True)
    
    url = f"https://myneta.info/LokSabha2024/{link}"
    
    if "show_constituencies" in link:  
        all_data = scrape_all_pages(driver, url)
    else:
        headers, rows = scrape_page(driver, url)
        if headers and rows:
            all_data = [headers] + rows
        else:
            all_data = []

    if all_data:
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        df.to_csv(os.path.join(state_dir, f"{constituency}.csv"), index=False)
        print(f"Data for {constituency} saved in {state_dir}/{constituency}.csv")

driver.quit()
