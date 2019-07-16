
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from time import sleep
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    # Set up the executable path and browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    news_title, news_text = get_news(browser) 

    mars_dict = {'news_title' : news_title, 
                  'news_text' : news_text}


    # Return results
    return mars_dict



def get_news(browser): 
    
    # Create base URLs
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    sleep(5)

    # Envoke beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Set base level list for the tag navigation
    div_news_title = soup.find('div', class_='content_title')
    div_news_text = soup.find('div', class_='article_teaser_body')


    latest_news_title =  div_news_title.text.strip()
    latest_news_text =  div_news_text.text.strip()
    
    # Check output
    print(latest_news_title)
    print(latest_news_text)


    
    browser.quit()


    return (latest_news_title, latest_news_text)


        
        
    
