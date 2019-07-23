'''
dataset to scrape
Name
address
ratings
causines
website
no of page search'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
from time import sleep
import random
import csv

'''options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")'''
CHROMEDRIVER_PATH = "C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver"
browser = webdriver.Chrome(CHROMEDRIVER_PATH)


def generate_random():  
  #It returns a random value between 3 and 5. That number indicates the seconds to be wait
  rand = random.randint(3, 5)
  return rand


def get_no_page():
  try:
    _page_no = browser.find_element_by_xpath(
        '//*[@id="search-results-container"]/div[2]/div[1]/div[1]/div/b[2]').text
    return(int(_page_no))
  except:
    return("cant access number of page results")


def extract_datasets(link):
  browser.get(link)
  sleep(generate_random())
  contents = soup(browser.page_source, "html.parser")
  all = contents.find_all("div", class_="content")
  for n in all:
    try:
      name = n.select("a.result-title.hover_feedback.zred.bold.ln24.fontsize0")[-1].text.strip()
    except:
      name = None
    try:
      address = n.find("b").text.strip()
    except:
      address = None
    try:
      ratings = n.select("div.ta-right.floating.search_result_rating.col-s-4.clearfix")[-1].span.text.strip()
    except:
      ratings= None
    try:
      causins_l = n.select("div.search-page-text.clearfix.row")[0].find_all("a")
      causinss = []
      for i in causins_l:
        causinss.append(i.text.strip())
      causins = ",".join(causinss)
    except:
      causins = None
    try:
      website = n.select("a.result-title.hover_feedback.zred.bold.ln24.fontsize0")[-1]['href']
    except:
      website = None

    csv_writer.writerow([name, address, ratings, causins, website])


url = 'https://www.zomato.com/laguna/don-jose-restaurants?category=2&ref_page=subzone'
browser.get(url)
print("%s page result found" %(get_no_page()))

pages = 2  # <how many pages to scrape

csv_file = open('restuarants', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Address', 'ratings', 'causins', 'website'])

for n in range(1,pages+1):
  page_links = "&page=%s" % (n)
  web_url = url+page_links
  extract_datasets(web_url)
  sleep(generate_random())

browser.quit()
csv_file.close()
