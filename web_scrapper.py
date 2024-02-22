from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json

# setup headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL to scrape 
url = "https://www.trendyol.com/pull-bear/siyah-casual-gunluk-spor-ayakkabi-p-355354920/yorumlar?boutiqueId=61&merchantId=112044&filterOverPriceListings=false&sav=true"
driver.get(url)
