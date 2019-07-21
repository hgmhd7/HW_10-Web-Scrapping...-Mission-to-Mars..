
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from time import sleep
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


# def init_browser():

#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     browser = Browser("chrome", **executable_path, headless=False)

#     return browser


def scrape_info():

    # Set up the executable path and browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    

    # Retieve the latest news title and text by calling on the get_news function \
    # and pass the browser to if to establish conection
    news_title, news_text = get_news(browser) 
    

    # Call the below function get the featured image\
    # and pass the browser to if to establish conection
    featred_mars_image = get_featured_image(browser)

    
    # Call the below funtion to get the weather report \
    # and pass the browser to if to establish conection
    mars_weather_report = weather_report(browser)


    # Call the below function to get the Mars Fact table \
    # and pass the browser to if to establish conection
    mars_fact_table_constructor = mars_facts_table(browser)


    # Call the below function to get the Mars hemisphere names \
    # and jpeg URLs and pass the browser to if to establish conection
    mars_hemisphere_dict = mars_hemispheres(browser)



    # Store the results into a dictionary
    mars_dict = {'news_title' : news_title, 
                 'news_text' : news_text,
                 'featred_mars_image' : featred_mars_image,
                 'mars_weather_report' : mars_weather_report,
                 'mars_fact_table_constructor' : mars_fact_table_constructor,
                 'mars_hemisphere_dict' : mars_hemisphere_dict}


    browser.quit()

    # Return results
    return (mars_dict)





def get_news(browser): 
    
    # Create base URLs
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    sleep(1)

    # Envoke beautiful soup
    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')

    # Set base level list for the tag navigation
    div_news_title = soup.find('div', class_='content_title')
    div_news_text = soup.find('div', class_='article_teaser_body')

    # Get the title and latest news 
    latest_news_title =  div_news_title.text.strip()
    latest_news_text =  div_news_text.text.strip()


    return (latest_news_title, latest_news_text)





def get_featured_image(browser): 
    

    # Create base URL and go to it
    featured_pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_pic_url)
    sleep(2)

    # # Envoke beautiful soup
    # featured_html = browser.html
    # soup = BeautifulSoup(featured_html, 'html.parser')

    # Save the Mars image path to the "featured_image_url" variable
    featured_image_url_navigation = (browser.click_link_by_partial_text('FULL IMAGE'), sleep(2),
    browser.click_link_by_partial_text('more info'), sleep(2),
    browser.click_link_by_partial_text('.jpg'), sleep(1))

    # Load the page UR into the featured_image_url variable
    featured_image_url = browser.url



    return (featured_image_url)


        
        
def weather_report(browser):

    # Create base URL and go to it
    mars_weather_url = 'https://twitter.com/marswxreport'
    browser.visit(mars_weather_url)
    sleep(1)


    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')



    # Find the base parent level for use within the loop
    tweets = soup.find_all('p', class_= "TweetTextSize")



    # Loop trough list to extract required info
    for tweet in tweets:
        
        # get the text for the tweet
        mars_weather = tweet.text.strip()
        
        # Only preint the first weather tweet, then break out of the loop
        if 'gusting' in mars_weather:
            
            break  


    return (mars_weather)    




def mars_facts_table(browser):


    # Set base URL
    mars_facts = 'https://space-facts.com/mars/'


    # Send URL to the read HTML funtion
    mf_table = pd.read_html(mars_facts)


    # Get the table index we want
    mars_facts_table = pd.DataFrame(mf_table[1])


    #Change column headers
    mars_facts_table.columns = ["Area of Observation", "Measurement"]


    # Convert table to HTML for use in our APP render
    mars_facts_table_html = mars_facts_table.to_html()



    return (mars_facts_table_html) 




def mars_hemispheres(browser):


    # Create base URL and go to it
    mars_weather_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_weather_url)


    # Envoke beautiful soup
    parent_hemi_html = browser.html
    soup = BeautifulSoup(parent_hemi_html, 'html.parser')



    # Set base/ parent level to loop through below
    hem_page = soup.find_all('h3')

    # Set empty list for the hemisphere URLS
    hemispheres_urls = []



    # Loop through list and get data
    for hemisphere in hem_page:
        
        # Get title and go to next page to retieve the jpg link for the hemisphere
        hem_title = hemisphere.text.strip()
        next_page = browser.click_link_by_partial_text(hem_title)
        sleep(2)
        
        
        # Envoke beautiful soup again so wwe can use that befor calling out find funtions\
        # This is done simple to now point to the new page we loaded and build a path as oppesed to artifact data
        hemi_html = browser.html
        soup = BeautifulSoup(hemi_html, 'html.parser')
        
        # # Find the class withthe URL
        div_hemi = soup.find('div', class_='downloads')
        
        # Finds the first 'a' tag that has a link
        link = div_hemi.find('a', href=True)
        
        #Debug statement
        #print(link['href'])
        
        
        # Add the new Hemisphere title and URL to a dictionary andn append to the hemispheres_urls = [] link
        hemispheres_urls.append({"title" : hem_title, "img_url" : link['href']})
        
        
        # Got back to the main URL to start the process over again
        browser.visit(mars_weather_url)


    
    return (hemispheres_urls)