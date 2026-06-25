from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time 
import random
import json

def setup_driver():
    """
    Sets up and initializes the Chrome WebDriver.

    - Configures Chrome binary location
    - Loads ChromeDriver service

    Returns:
    webdriver.Chrome: Configured Chrome WebDriver instance
    """
    options = Options()
    options.binary_location = r'C:\\Program Files\\chrome-win64\\chrome.exe'
    
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def get_product_detail(url):
    
    """
    Fetches individual book detail page using requests and extracts the table data
    
    Args:
    url (str): URL of the book detail page
    
    Returns:
    table_data (dict): Dictionary of book details 
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        rows = soup.select('table.table.table-striped tr')
        table_data={}
        
        for row in rows:
            header = row.find('th').text.strip()
            value = row.find('td').text.strip()
            table_data[header]=value
            
        return table_data
    except Exception as e:
        print(f'Error: {e} | URL:{url}')
        return {}
    

def get_page(driver):
    """
    Extracts book data from the current page using Selenium.

    - Waits for page elements to load
    - Extracts title, star_rating, and product link
    - Calls get_product_detail() for additional data

    Args:
    driver (webdriver.Chrome): Active Selenium WebDriver
    
    Returns: 
    page_data[dict]: List of dictionaries containing book data for the page
    """
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product_pod')))
    to_num = {
        'One':1, 
        'Two':2,
        'Three':3,
        'Four':4,
        'Five':5
        }
    books = driver.find_elements(By.CLASS_NAME, 'product_pod')
    page_data=[]

    for book in books:
        title = book.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('title')
        rating_class = book.find_element(By.CLASS_NAME, 'star-rating').get_attribute('class')
        star_rating = rating_class.split()[-1]
        star_rating = to_num.get(star_rating, 0)
        link = book.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
        table_data = get_product_detail(link)
        book_data = {'title':title,
                     'star_rating':star_rating,
                     'link': link}
        book_data.update(table_data)
        page_data.append(book_data)
        
    return page_data

def click_next(driver):
    """
    Clicks the 'Next' button to navigate to the next page.

    Args:
    driver (webdriver.Chrome): Active Selenium WebDriver

    Returns:
    (bool): True if next page exists and was clicked, False otherwise
    """
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'next')
        next_button.find_element(By.TAG_NAME, 'a').click()
        return True
    
    except:
        return False
    
def get_all_pages(driver, start_url):
    """
    Iterates through all pages and collects book data.

    - Navigates through pagination
    - Calls get_page() for each page
    - Adds random delay between requests

    Args:
    driver (webdriver.Chrome): Active Selenium WebDriver
    start_url (str): Starting URL for scraping

    Returns:
    list[dict]: Combined list of all book data across pages
    """
    driver.get(start_url)
    all_data=[]
    page=1
    while True:
        print(f'Scraping page {page}')
        data = get_page(driver)
        all_data.extend(data)
        page+=1
        has_next = click_next(driver)
        
        if not has_next:
            print('Done!')
            break
        time.sleep(random.uniform(1, 3))
        
    return all_data
       
def save_to_json(data, filename):
    """
    Saves scraped data to a JSON file.

    Args:
    data (list[dict]): Scraped book data
    filename (str): Output JSON file name

    Returns:
    None
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    """
    Main execution function.

    - Initializes WebDriver
    - Starts scraping process
    - Saves results to JSON
    - Closes browser

    Returns:
    None
    """
    
    driver = setup_driver()
    url = 'https://books.toscrape.com/' 
    data = get_all_pages(driver, url)
    save_to_json(data, 'books.json')
    driver.quit()

if __name__=='__main__':
    main() 


        
        
        
        
