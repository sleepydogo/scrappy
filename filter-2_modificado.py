# Este filtro deja solo los numeros que tienen whatsapp
#   Author: Sleepydogo

## Este filtro solo procesa los numeros de paraguay

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import os

def init_selenium():
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def load_phones(filename):
    data = pd.read_excel(filename)
    data.iloc[:, 3] = data.iloc[:, 3].astype(str)
    return data
    
def existe_en_whatsapp(phone, driver):
    input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[1]/div/div/div[2]/input')
    time.sleep(1)
    input.send_keys('+')
    input.send_keys(phone)
    time.sleep(3) 
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[2]/div[2]/div[2]')
        input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.8)
        input.send_keys(Keys.DELETE)
        return True
    except:
        input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.8)
        input.send_keys(Keys.DELETE)
        return False
        

# 30 segundos para iniciar sesion
def open_whatsapp(driver):
    driver.get('https://web.whatsapp.com/')
    time.sleep(30)
    three_dots = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div/span')
    three_dots.click()
    time.sleep(2)
    new_group = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/span/div/ul/li[1]/div')
    new_group.click()
    time.sleep(2)

def filter(table, driver):
    for index, row in table.iterrows():
        phone = row[3]
        if not existe_en_whatsapp(phone, driver):
            table = table.drop(index)
            print(phone)
        else:
            print(f' {phone} ---> ok')
    return table
    
def main():
    # Abro el navegador
    driver = init_selenium()
    ## Inicio sesion en whatsapp
    open_whatsapp(driver)
    # Cargo los telefonos
    table = load_phones('Paraguay/3-solo_paraguay.xlsx')

    table = filter(table, driver)     
    
    table = table.drop(table.columns[0], axis=1)

    table.to_excel('Numeros Paraguayos con whatsapp.xlsx')    
    print('----listo.')
    
    #driver.close()
    return 1 


if __name__ == '__main__':
    main() 