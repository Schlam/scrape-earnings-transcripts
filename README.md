# ~~Seeking~~ Scraping Alpha
---


This repository contains a script, a notebook and a collection of text files.

The notebook shows the steps taken to set up this pipeline, and allows for easier modifications.

This script that can theoretically scrape through the entire collection of earnings call transcripts made available on Seeking Alpha's [earnings](https://seekingalpha.com/earnings/earnings-call-transcripts) page, but in its present state only collects data from the transcripts listed on page 1.

The file collection shows how the transcript dialogue is formatted, but contains unfinished sample results only. Those you'll have to scrape for yourself. These were generated by running the exact code provided here sans one line which follows a link to "Single page view" present on the transcript page.

**This script requires [splinter](https://splinter.readthedocs.io/en/latest/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)**, if you do not have those packages installed then follow the install instructions included in their respective documentation.



##### Using this script is very straightforward:


On the command line, type ```python scrape_alpha.py``` and hit enter

If desired, you can change the ```SECTOR``` at the top of the code to match any of the following:
  
    - 'all' (contains transcripts from public companies around the world)
    - 'popular' (default option)
    - 'basic-materials'
    - 'conglomerates'
    - 'consumer-goods'
    - 'financial'
    - 'healthcare'
    - 'industrial-goods'
    - 'services'
    - 'technology'
    - 'utilities'

An instance of Chrome seperate from any existing chrome instance you might have running will pop up: you have 45 seconds to log into SA by clicking "Sign in" in the top right corner of the webpage.* **


*<sub> If needed, you can add more time by adjusting LOGIN_DELAY found at the top of the python file</sub>

**<sub> One might be able to use splinter to automate this process using the ```browser.fill``` method<sub>


**Logging in is crucial**, otherwise you'll be prompted to sign in on the page containing the transcript and this will cause the html code our script expects to be different. The sign in process can be automated using browser.fill() (see splinter docs.) 

Once logged in, the process will start to take place! If you're lucky, the script will run its course before the website's bot-detection measures grow skeptical and prompt you to hold down a button for two seconds


###### It's worth noting that on many websites, repeated requests for data from the site can possibly lead to an IP ban. 

###### Be careful-- especially if modifying/debugging the code and making repeated identical requests.