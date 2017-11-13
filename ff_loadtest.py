import time
import csv
import random
import json
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# define unique results file for this run
ts = int(time.time())
filename = "perftimings_firefox_" + str(ts) + ".csv"

# initialize Firefox options
ff_options = Options()

# Enables private browsing for testing
# comment this line if you want to test normal Firefox mode
ff_options.add_argument("-private")

# Select path to Firefox binary
# this is the default path on macOS
ff_binary = '/Applications/Firefox.app/Contents/MacOS/firefox'

# open list of urls for testing
with open('news.txt', 'r') as url_file:
    test_urls = url_file.readlines()

# do 10 runs
for x in range(0,10):
    
    # start geckodriver using the previously defined options and binary
    driver = webdriver.Firefox(firefox_options=ff_options, firefox_binary = ff_binary )
    
    # set page load time out to 60 seconds
    driver.set_page_load_timeout(60)
    
    # randomly shuffle list of urls to avoid order bias in testing
    random.shuffle(test_urls)

    for i, url in enumerate(test_urls):
                    
        try:
            # request url from list
            driver.get(url)
            
            # pull window.performance.timing after loading the page and add information about url and number of run
            perf_timings = driver.execute_script("return window.performance.timing")
            perf_timings['url'] = str(url)
            perf_timings['run'] = str(x)
            
            # write perf_timings to results csv file
            if os.path.exists(filename):
                #append_write = 'a' # append if already exists
                with open(filename, 'a') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(perf_timings.values())
            else:
                #append_write = 'w' # make a new file if not
                with open(filename, 'w') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(perf_timings.keys())
                    csvwriter.writerow(perf_timings.values())


        except: # what to do in case that an exception is thrown (which happens usually upon page load timeout)

            # also pull data and store it to the results file
            perf_timings = driver.execute_script("return window.performance.timing")
            perf_timings['url'] = str(url)
            perf_timings['run'] = str(x)
            
            if os.path.exists(filename):
                #append_write = 'a' # append if already exists
                with open(filename, 'a') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(perf_timings.values())
            else:
                #append_write = 'w' # make a new file if not
                with open(filename, 'w') as results_file:
                    csvwriter = csv.writer(results_file)
                    csvwriter.writerow(perf_timings.keys())
                    csvwriter.writerow(perf_timings.values())

            continue
			  
    driver.quit()