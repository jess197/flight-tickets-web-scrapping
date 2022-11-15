from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd 
from bs4 import BeautifulSoup
import os 


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

to_location = 'NYC'
url = 'https://www.kayak.com.br/flights/CWB-{to_location}/2023-06-15/2023-06-29/2adults?sort=price_a'.format(to_location=to_location)

driver.get(url)
wait = WebDriverWait(driver, 100)
sleep(10)

flight_rows = driver.find_elements(by=By.XPATH, value='//div[@class="inner-grid keel-grid"]')
#print(flight_rows)

lst_prices = []
lst_company_names = []
lst_depart_time = []
lst_arrival_time = []
lst_going_time = []

for WebElement in flight_rows: 
    elementHTML = WebElement.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML,'html.parser')

    #price
    temp_price = elementSoup.find("div", {"class":"col-price result-column js-no-dtog"})
    price = temp_price.find("span", {"class":"price-text"})
    lst_prices.append(price.text)

    # hand luggage

    # company names
    company_names = elementSoup.find("span", {"class":"codeshares-airline-names"}).text
    lst_company_names.append(company_names)

    # depart time 
    depart_time = elementSoup.find("span", {"class":"depart-time base-time"}).text
    lst_depart_time.append(depart_time)

    arrival_time = elementSoup.find("span", {"class":"arrival-time base-time"}).text
    lst_arrival_time.append(arrival_time)


    temp_times = elementSoup.find("div", {"class":"section times"})
    times = temp_times.find("div", {"class":"top"})
    lst_going_time.append(times.text)


for i in range(len(lst_prices)):
   price = 'Price: '+str(lst_prices[i]).strip('[]').lstrip().rstrip()
   going_time = 'Departure/Arrival: '+str(lst_going_time[i]).strip('[]').lstrip().rstrip().replace('\n',' ')
   company_name = 'Company Name: '+str(lst_company_names[i]).strip('[]').lstrip().rstrip()
   print(company_name+' - '+price+' - '+going_time)








