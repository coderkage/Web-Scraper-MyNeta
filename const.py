from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time, re

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://myneta.info/LokSabha2024/'
driver.get(url)
time.sleep(2)

page_source = driver.page_source

driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')
data = []

states = soup.find_all('div', class_='w3-dropdown-click')

for state in states:
    state_button = state.find('button', class_='dropbtnJS')
    state_name = state_button.get_text(strip=True)
    state_id = state_button.get('onclick').split("'")[2]
    
    dropdown_content = state.find('div', class_='w3-dropdown-content')
    links = dropdown_content.find_all('a', class_='w3-bar-item')
    
    for link in links:
        href = link.get('href')
        constituency_name = link.get_text(strip=True)
        
        if 'show_constituencies' in href:
            all_constituencies_link = href
            data.append([state_name, state_id, 'ALL CONSTITUENCIES', all_constituencies_link])
        elif 'show_candidates' in href:
            constituency_link = href
            data.append([state_name, state_id, constituency_name, constituency_link])

df = pd.DataFrame(data, columns=['State Name', 'State ID', 'Constituency', 'Constituency Link'])
def extract_state_id(link):
    match = re.search(r'state_id=(\d+)', link)
    if match:
        return match.group(1)
    return None

df['State ID'] = df['Constituency Link'].apply(extract_state_id)
df['State ID'] = df['State ID'].ffill()

df.to_csv('constituencies.csv', index=False)

print("CSV file created successfully.")
