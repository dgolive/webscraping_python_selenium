# -*- encoding: utf-8 -*-

# source: https://github.com/gabrielfroes/webscraping_python_selenium/tree/master
# NBA Top 10 - Season 2023-24
# modified by: dgolive

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

# Grab content from URL 
url = "https://www.nba.com/stats/players/traditional"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'DREB', 'label': 'DREB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}

def buildrank(type):
    
    field = rankings[type]['field']
    label = rankings[type]['label']

    driver.find_element(By.XPATH, value=f"//*[@id='__next']//table//thead//tr//th[@field='{field}']").click()
   
    element = driver.find_element(By.XPATH, value='//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table')                                                      
  
    html_content = element.get_attribute('outerHTML')

    # Parse HTML contect with BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')  
    table = soup.find(name='table')

    # Data Structure Conversion with Pandas Dataframe
    df_full = pd.read_html(str(table))[0].head(10)  # Top 10
    df = df_full[['Unnamed: 0', 'Player', 'Team', label]]  # Clean Up unnecessary columns
    df.columns = ['pos', 'player', 'team', 'total']

    # Convert to Dictionary 
    return df.to_dict('records')

# option = Options()
# option.headless = True
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]').click()  # accept cookies

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Dump and save to JSON file
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)
