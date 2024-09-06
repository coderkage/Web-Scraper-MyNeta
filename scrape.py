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


# Read the CSV file
csv_file = 'constituencies.csv'
data = pd.read_csv(csv_file)

# Initialize an empty list to store all data
final_data = []

# Keep track of processed states
processed_states = set()

# Process each row
for _, row in data.iterrows():
    state_name = row['State Name']
    state_id = row['State ID']
    link = row['Constituency Link']
    
    # Only process the first link for each state
    if state_name in processed_states:
        continue
    
    # Mark the state as processed
    processed_states.add(state_name)
    
    # Generate URL for scraping
    url = f"https://myneta.info/LokSabha2024/{link}"
    
    # Scrape data (assuming the first link needs to scrape all pages)
    all_data = scrape_all_pages(driver, url)
    
    # Add state name to each row of data
    if all_data:
        headers = all_data[0] + ['State Name']
        rows_with_state = [row + [state_name] for row in all_data[1:]]
        final_data.extend(rows_with_state)
        
# Save all data to a single CSV file
if final_data:
    df = pd.DataFrame(final_data, columns=headers)
    df.to_csv('all_states_data.csv', index=False)
    print("Data saved to all_states_data.csv")

driver.quit()
