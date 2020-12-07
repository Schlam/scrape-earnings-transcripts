from splinter import Browser
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from time import sleep
import requests 
import os



# Number of seconds to delay script start/pause between requests
LOGIN_DELAY, WAIT_TIME = 45, 5

SECTOR = "most-popular"
URL = f"https://seekingalpha.com/earnings/earnings-call-transcripts?sector={SECTOR}"



def config_browser():
    """
    
    Configure the automated browser used for scraping
    
    """

    # Set path to chromedriver, set headless=False
    chrome_config = {
        "executable_path": "/usr/local/bin/chromedriver",
        "headless": False, # if headless, then no browser is displayed
    }
    
    return Browser('chrome', **chrome_config)


def get_elements(soup):
    """
    
    Get page elements specific to each Earnings Call
    
    """

    elements = soup.find(
        'ul', {'id':'analysis-list-container'})\
            .find('ul')\
                .find_all('li')

    return elements


def get_urls(elements):
    """
    
    Iterate through relative urls found in
    each element and return a list of full urls
    
    """
    
    urls = [
        "https://seekingalpha.com" + \
        
        element.find("h3")\
            .find("a")\
                .get("href")

        for element in elements
    ]
    
    return urls


def get_tickers(elements):
    """ 
    
    For each earnings call, extract 
    ticker from its associated webpage element
    
    """
    
    # Get text from element
    link_text = [
        element.find("h3")\
            .find("a")\
                .get_text()
        for element in elements]
    
    # Get symbol from text
    tickers = [text[text.find('(')+1:text.find(')')]
               for text in link_text]
    
    return tickers


def get_dates(urls):
    """
    
    Extract quarter/fiscal year from the url address
    
    """
    
    dates = []
    
    for url in urls:
        
        # Get index for str pattern preceding quarter/date
        index = url.find('-on-q')
        

        if index == -1:

            # Account for urls that do not match the pattern    
            dates.append('unknown_date')
        
        else:
        
            # Get index range for date pattern
            date_start, date_end = index + 4, index + 11
        
            # Slice url for date and add to list
            date = url[date_start: date_end].replace('-','_')
            dates.append(date)
        
    return dates


def get_filenames(symbols,dates):
    """
    
    Create folder structure and generate filenames using 
    the date and symbol for each relevant ticker
    
    """

    # Get date and time of when scraping was performed
    datetime_dir = str(datetime.today())

    # Make directory for this scraping instance
    os.mkdir(f'transcripts/{SECTOR}/{datetime_dir}')

    # Get filenames for each text file
    filenames = [
        f"transcripts/{SECTOR}/{datetime_dir}/{symbol}_{date}.txt"
        for symbol, date in zip(symbols, dates)
    ]

    return filenames


def get_transcript(url, browser):
    """
    
    This function
        -   visits the transcript webpage
        -   clicks "Single page view" to get full transcript (if necessary)
        -   parses webpage for paragraph elements
        -   joins together text from those elements
        -   returns the full transcript
    
    """
    # Visit url, wait for page to load
    browser.visit(url)
    sleep(1.5)
    
    try:

        # Attempt to click 'Single page view' link
        browser.links\
            .find_by_partial_text('Single page view')\
                .click()
        
        # wait for page to load
        sleep(1)

    except Exception as e:
        
        print(f"{type(e)}: {e}")
        print("'Single page view' link not present on webpage, moving on")


    # Get html from webpage, extract content from html
    soup = Soup(browser.html, 'html.parser')
    content = soup.find('div', {'id':'main_content'})
    
    # Join text from each paragraph element
    text = '\n'.join([
        element.get_text() for element in 
        content.find_all('p')])
    
    return text


def write_text_to_file(text,fname):
    """ 

    Write text to text file named after the
    company's ticker and date of the call
    
    """
    with open(fname, 'w') as f:
            f.write(text)


def scrape_all_transcripts(browser, url=URL):
    """
    
    This function:
        -   visits the page containing a list of earnings call transcripts
        -   extracts the url address for each earnings call
        -   visits each url and extracts the transcript dialogue
        -   saves the transcript as a .txt file in the format <TICKER>_<QUARTER>_<YEAR>.txt
    
    """


    # Visit webpage, parse the html, and wait for user login
    browser.visit(url)
    soup = Soup(browser.html, 'html.parser')
    
    sleep(LOGIN_DELAY)
    

    # Get elements, and parse for links
    transcript_elements = get_elements(soup)
    transcript_urls = get_urls(transcript_elements)
    
    # Extract ticker symbol, and date of earnings call 
    ticker_symbols = get_tickers(transcript_elements)
    call_dates = get_dates(transcript_urls)

    # Generate filenames for each transcript using date/symbol
    filenames = get_filenames(ticker_symbols, call_dates)


    # Count failed attempts for data logging purposes
    error_no = 0

    # Iterate through earnings call transcript urls/filenames
    for url, filename in zip(transcript_urls, filenames):

        try:

            # Get transcript from webpage
            text = get_transcript(url, browser)
        
            # Attempt to write transcript to text file
            write_text_to_file(text, filename)
            print(f"successfully wrote file: {filename}")
        

        except Exception as e:

            # Add one to error count
            error_no += 1

            # If writing file fails, show error message and continue
            print(f"Error writing data to {filename}, {type(e)}:{e}")
            print(f"{error_no}/{len(transcript_urls)} files not written")
        
        # Give the servers a break!!
        sleep(WAIT_TIME)


if __name__ == "__main__":


    # Configure browser 
    browser = config_browser()

    # Scrape all transcripts
    scrape_all_transcripts(browser)
    
    # Quit browser 
    browser.quit()