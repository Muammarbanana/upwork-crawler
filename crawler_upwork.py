from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import csv
import re
from csv import writer

chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--user-data-dir=C:/Users/Acer/AppData/Local/Google/Chrome/User Data')
# chrome_options.add_argument('--profile-directory=Profile 1'),
# chrome_options.add_argument('--headless')

print('Enter keyword: ')
keyword = input()

url = f'https://www.upwork.com/nx/jobs/search/?q={keyword}&sort=recency'

driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver",)

driver.get(url)
time.sleep(2)

counter = 0

#open document and start writing process
with open('DataJobUpwork.csv','a', encoding="utf16", newline='') as fd:
    csv_writer = writer(fd, delimiter=",")

    # write title
    csv_writer.writerow([
                'Job Title',
                'Job Type',
                'Contractor Tier'
                ])

    while True:

        # wait content to be loaded
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[class='my-0 p-sm-right job-tile-title'] > a")))

        # detect next button
        nextButton = driver.find_elements(By.CSS_SELECTOR, "button[class='up-pagination-item up-btn up-btn-link'] > div[class='next-icon up-icon']")

        # take web element
        jobTitle = driver.find_elements(By.CSS_SELECTOR, "h3[class='my-0 p-sm-right job-tile-title'] > a")
        jobType = driver.find_elements(By.CSS_SELECTOR, "strong[data-test='job-type']")
        contractorTier = driver.find_elements(By.CSS_SELECTOR, "span[data-test='contractor-tier']")
        # write data to document
        for el in range(len(jobTitle)):
            csv_writer.writerow([
                jobTitle[el].text,
                jobType[el].text,
                contractorTier[el].text
                ])
            
        # detect next button disabled
        if (len(nextButton) == 0):
            break          
        
        # move to next page
        nextButton[0].click()
        time.sleep(2)

        counter += 1
        print('page: ' + str(counter))


            