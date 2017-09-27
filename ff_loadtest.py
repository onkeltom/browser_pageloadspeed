import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import csv
import json

ts = int(time.time())

filename = "perftimings" + "_firefox_cold_DSL" + str(ts) + ".csv"

ff_options = Options()

ff_binary = '/Applications/Firefox Beta.app/Contents/MacOS/firefox'
#ff_binary = '/Applications/FirefoxNightly.app/Contents/MacOS/firefox'

# Private browsing
ff_options.add_argument("-private")
#ff_options.setBinary('/Applications/FirefoxNightly.app/Contents/MacOS/firefox')

with open('news.txt', 'r') as url_file:
    test_urls = url_file.readlines()

for x in range(0,50):
    print(x+1)
    
    driver = webdriver.Firefox(firefox_options=ff_options, firefox_binary = ff_binary )  # Optional argument, if not specified will search path.
    
#    print x
    
    driver.set_page_load_timeout(30)

    for i, url in enumerate(test_urls):
                    
        try:
            driver.get(url)
            navStart = driver.execute_script("return window.performance.timing")
            navStart['url'] = url
            navStart['run'] = str(x)
            
            if x == 0 and i == 0:
                with open(filename, 'wb') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(navStart.keys())
                    csvwriter.writerow(navStart.values())
            else:
                with open(filename, 'a') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(navStart.values())


        except:
            navStart = driver.execute_script("return window.performance.timing")
            navStart['url'] = url
            navStart['run'] = str(x)
            
            with open(filename, 'a') as results_file:
                csvwriter = csv.writer(results_file)
                csvwriter.writerow(navStart.values())

            continue
			  
    driver.quit()