from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    
    def start_browser():
        path = {'executable_path': ChromeDriverManager().install()}
        return Browser('chrome', **path, headless=False)

    #IMPORT DEPENDENCIES AND INITIALIZE BROWSWER

    browser = start_browser()
    browser.visit('https://mars.nasa.gov/news/')
    html = browser.html
    nasa_soup = bs(html, "html.parser")
    nasa_news_element = nasa_soup.find_all('li', class_='slide')[0]
    title = nasa_news_element.find('div', class_='content_title').text
    description = nasa_news_element.find('div', class_='rollover_description_inner').text
    print(title)
    print(description)

    #CALL BROWSER, PARSE INTO SOUP, FIND TITLE AND DESCRIPTION, SAVE AS VARIABLES, PRINT

    initial_df = pd.read_html("https://space-facts.com/mars/")
    df = initial_df[0]
    df_html = df.to_html(index=False)

    #READ URL AS HTML, SET DATAFRAME EQUAL TO TABLE ON PAGE, TURN TO HTML

    browser = start_browser()
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    img_links = browser.find_by_css("a.product-item h3")
    link_count = len(img_links)

    urls = []
    titles = []
    url_title_dicts = []

    for i in range(link_count):
        browser.find_by_css("a.product-item h3")[i].click()
        hem = browser.links.find_by_text("Sample").first
        urls.append(hem['href'])
        titles.append(browser.find_by_css('h2.title').text)
        browser.back()

    for j in range(len(titles)):
        dict_var = {}
        dict_var['title'] = titles[j]
        dict_var['url'] = urls[j]
        url_title_dicts.append(dict_var)

    print (url_title_dicts)

    #CALL BROWSER, FIND IMAGE LINK ELEMENTS, LOOP THROUGH IN ORDER TO GATHER ALL TITLES AND URLS FOR ELEMENTS, LOOP THROUGH LISTS TO CREATE LIST OF DICTS



    master_dict = {
    'Article' : title,
    'Article_Description' : description,
    'Data_Table' : df_html,
    'Hemispheres' : url_title_dicts
    }
    return master_dict

    import pymongo

    client = pymongo.MongoClient()
    db = client.mars
    col = db.data

    col.insert_one(master_dict)

    #CREATE FINAL OUTPUT DICT