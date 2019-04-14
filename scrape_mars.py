from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time
from flask import Flask
import cssutils
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':'/webdrivers/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

marsnews = {}

def scrape1():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find(class_='content_title').find('a').text
    news_p = soup.find(class_='article_teaser_body').text

    marsnews['news_title'] = news_title
    marsnews['news_p'] = news_p

    browser.quit()

    return marsnews

def scrape2():
    browser = init_browser()

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)
    time.sleep(5)

    html = browser.html
    soup1 = BeautifulSoup(html, "html.parser")

    find_main = soup1.findAll('a')[1]
    main_url = "https:" +  find_main['href']
    image_url = soup1.find('article')['style']
    style = cssutils.parseStyle(image_url)
    url = style['background-image']
    url1 = url.replace('url(/', '').replace(')', '')
    featured_image_url = main_url+url1
    
    marsnews['featured_image_url'] = featured_image_url

    browser.quit()
    return marsnews

def scrape3():
    browser = init_browser()

    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    data = requests.get(url2) 
    time.sleep(5)

    all_tweets = []
    html = BeautifulSoup(data.text, 'html.parser')
    timeline = html.select('#timeline li.stream-item')
    for tweet in timeline:
        tweet_text = tweet.select('p.tweet-text')[0].get_text()
        if "sol" in tweet_text:
            all_tweets.append(tweet_text)    
    
    mars_weather = all_tweets[0]
    
    marsnews['mars_weather'] = mars_weather

    browser.quit()

    return marsnews

def scrape4():
    
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    tables

    df = tables[0]
    df.columns = ['Description', 'Results']
    df.head()

    df.set_index('Description', inplace=True)
    df.head()
    html_table = df.to_html()
    table = html_table.replace('\n', '')
    
    marsnews['table'] = table

    return marsnews

def scrape5():
    browser = init_browser()
    
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(5)
    
    html = browser.html
    
    soup2 = BeautifulSoup(html, 'html.parser')
    
    titles = soup2.body.find_all('h3')
    
    title = []
    image_url= []

    for x in titles:
        title.append(x.text)
    
    for title_url in title:
        browser.click_link_by_partial_text(title_url)
        
        html = browser.html
        
        soup = BeautifulSoup(html, 'html.parser')
        
        url = soup.find('img', class_ = 'wide-image')
        image_url.append('https://astrogeology.usgs.gov' + url["src"])
        browser.click_link_by_partial_text('Back')
        keys  = ["title", "img_url"] 
        hemisphere_image_urls = [dict(zip(keys,values)) for values in zip(title,image_url)]

        marsnews['images'] = hemisphere_image_urls
    
    browser.quit()

    return marsnews
