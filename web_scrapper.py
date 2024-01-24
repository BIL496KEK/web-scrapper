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

# time to load the page depending on the connection speed
scroll_pause_time = 0.4

# get the screen height of the web
screen_height = driver.execute_script(
    "return window.screen.height;")

# get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# scroll till the end of the page
i = 1
while True:
    # scroll one screen height each time
    driver.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# extract text from <p> tags inside <div> with class 'comment-text'
comments = []
for div in soup.find_all("div", class_="comment-text"):
    for p in div.find_all("p"):
        comments.append(p.text.strip())

# extract the text from span tags within divs with class='rnr-com-like'
like_count = []
for div in soup.find_all("div", class_="rnr-com-like"):
    span = div.find("span")
    if span:
        text = span.text.strip()  # Clean up the text
        # Extract the number inside parentheses
        if text.startswith('(') and text.endswith(')'):
            number = text[1:-1].strip()
            if number.isdigit():  # Add to the list if it's a numeric value
                like_count.append(number)


# combine each comment and its like count into a dictionary
data = [{"comment": comments[j], "likes": like_count[j]} for j in range(len(comments))]

# write to a JSON file
with open('output_file.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
