import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import json

chrome_options = Options()

# Private browsing
chrome_options.add_argument("--incognito")

ts = int(time.time())
filename = "perftimings" + "_chrome_cold_DSL_" + str(ts) + ".csv"

with open('news.txt', 'r') as url_file:
    test_urls = url_file.readlines()

for x in range(0,50):
    driver = webdriver.Chrome(chrome_options=chrome_options)  # Optional argument, if not specified will search path.
    
    print x
    
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