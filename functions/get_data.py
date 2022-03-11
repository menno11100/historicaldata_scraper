from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
import json

import time

from random import seed
from random import random
import numpy as np
import pickle
import pandas as pd


options = Options()
options.headless = False
options.add_argument('log-level=2')
options.add_argument(
    '--ignore-certificate-errors')  # https://stackoverflow.com/questions/37883759/errorssl-client-socket-openssl-cc1158-handshake-failed-with-chromedriver-chr
options.add_argument(
    '--ignore-ssl-errors')  # https://stackoverflow.com/questions/37883759/errorssl-client-socket-openssl-cc1158-handshake-failed-with-chromedriver-chr
options.add_argument("--start-maximized")
options.add_argument("--incognito")
# Bron: https://stackoverflow.com/questions/53998690/downloading-a-pdf-using-selenium-chrome-and-python
options.add_experimental_option('prefs', {
    "download.default_directory": "/Users/mennohuijbregts/Downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

def get_data():
    driver = webdriver.Chrome(options=options)
    date_excepted = [20150917]


    dates_to_retrieve = json.load(open('dates.json'))
    dates_retrieved = json.load(open('data/dates_retrieved.json'))

    with open('data/price.pkl', 'rb') as f:
        price_dict = pickle.load(f)
    with open('data/supply.pkl', 'rb') as f:
        supply_dict = pickle.load(f)
    with open('data/volume.pkl', 'rb') as f:
        volume_dict = pickle.load(f)    
    with open('data/marketcap.pkl', 'rb') as f:
        marketcap_dict = pickle.load(f)
    with open('data/index.pkl', 'rb') as f:
        index_dict = pickle.load(f)

    for (count, date) in enumerate(dates_to_retrieve):
        y = 1000
        if date not in dates_retrieved and date not in date_excepted:
            try:
                print(f'start - {date}')
                url = 'https://coinmarketcap.com/historical/'+str(date)
                driver.get(url)

                for r in range(0, 200):
                    mytable = driver.find_elements_by_class_name("cmc-table-row")
                    columns = mytable[r].find_elements_by_css_selector('td')

                    while len(columns) < 4:
                        seed(1)
                        y = y+500+random()
                        driver.execute_script("window.scrollTo(0, "+str(y)+")")

                        time.sleep(.03)

                        mytable = driver.find_elements_by_class_name("cmc-table-row")
                        columns = mytable[r].find_elements_by_css_selector('td')

                    index = columns[0].text
                    ticker = columns[2].text + '-' + columns[1].text
                    price = columns[4].text[1:]
                    marketcap = columns[3].text[1:]
                    volume = columns[6].text[1:]
                    supply = columns[5].text

                    if ticker in price_dict.keys():
                        price_dict[ticker] = np.append(price_dict[ticker][:len(dates_retrieved)], price)
                        volume_dict[ticker] = np.append(volume_dict[ticker][:len(dates_retrieved)], volume)
                        marketcap_dict[ticker] = np.append(marketcap_dict[ticker][:len(dates_retrieved)], marketcap)
                        supply_dict[ticker] = np.append(supply_dict[ticker][:len(dates_retrieved)], supply)
                        index_dict[ticker] = np.append(index_dict[ticker][:len(dates_retrieved)], index)
                    else:
                        nan_array = np.empty([1,len(dates_retrieved)])
                        if len(nan_array) > 0: nan_array[:] = np.nan
                        price_dict[ticker] = nan_array
                        volume_dict[ticker] = nan_array
                        marketcap_dict[ticker] = nan_array
                        supply_dict[ticker] = nan_array
                        index_dict[ticker] = nan_array
                        
                        price_dict[ticker] = np.append(price_dict[ticker][:len(dates_retrieved)], price)
                        volume_dict[ticker] = np.append(volume_dict[ticker][:len(dates_retrieved)], volume)
                        marketcap_dict[ticker] = np.append(marketcap_dict[ticker][:len(dates_retrieved)], marketcap)
                        supply_dict[ticker] = np.append(supply_dict[ticker][:len(dates_retrieved)], supply)
                        index_dict[ticker] = np.append(index_dict[ticker][:len(dates_retrieved)], index)


                # Add date to dates retrieved.      
                dates_retrieved.append(date)
                print(f'end - {date}')
            except:
                print(f"Error occured at {date}")
                break


            # Add NaN for missing days
            for i in price_dict:
                if len(price_dict[i]) < len(dates_retrieved):
                    price_dict[i] = np.append(price_dict[i], np.nan)
                    volume_dict[i] = np.append(volume_dict[i], np.nan)
                    supply_dict[i] = np.append(supply_dict[i], np.nan)
                    marketcap_dict[i] = np.append(marketcap_dict[i], np.nan)
                    index_dict[i] = np.append(index_dict[i], np.nan)
                elif len(price_dict[i]) > len(dates_retrieved):
                    print('-------SOMETHING WRONG -------')

            # Save as pickle
            if count%5 == 0:
                with open('data/price.pkl', 'wb') as handle:
                    pickle.dump(price_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('data/supply.pkl', 'wb') as handle:
                    pickle.dump(supply_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('data/volume.pkl', 'wb') as handle:
                    pickle.dump(volume_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('data/marketcap.pkl', 'wb') as handle:
                    pickle.dump(marketcap_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('data/index.pkl', 'wb') as handle:
                    pickle.dump(index_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('data/dates_retrieved.json', 'w') as fp:
                    json.dump(dates_retrieved, fp,  indent=4)
                print('saved')
    print('Done')