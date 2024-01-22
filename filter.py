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


#   Elementos del HTML 
# 
# tres puntos
# /html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div/span
# 
# nuevo grupo
# /html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/span/div/ul/li[1]/div
# 
# input
# /html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[1]/div/div/div[2]/input
# 
# contacto
# /html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[2]/div[2]/div[2]

def init_selenium():
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options)
    return driver

def load_phones(filename):
    data = pd.read_excel(filename)
    # Eliminamos la primera columna de indices
    data = data.iloc[:, 1:]
    return data

def delete_rows_with_no_phones(data):
    data = data[~data['Telefono'].astype(str).str.contains('#')]
    data = data[~data['Telefono'].astype(str).str.contains('[a-zA-Z]')]
    return data

def filter(table, driver):
    for index, row in table.iterrows():
        phone = row['Telefono']
        if not existe_en_whatsapp(phone, driver):
            # Si la función existe() retorna False, elimina la fila
            table = table.drop(index)
            print(phone)
        else:
            print(phone + '--> Ok')
    return table
    
def existe_en_whatsapp(phone, driver):
    input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[1]/div/div/div[2]/input')
    time.sleep(1)
    input.send_keys(phone)
    time.sleep(3) 
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[2]/div[2]/div[2]')
        input.send_keys(Keys.COMMAND + "a")
        time.sleep(0.8)
        input.send_keys(Keys.DELETE)
        return True
    except:
        input.send_keys(Keys.COMMAND + "a")
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



def main():
    driver = init_selenium()
    open_whatsapp(driver)
    ruta_actual = os.getcwd()
    ruta_datos = os.path.join(ruta_actual, "datos2")
    for carpeta in os.listdir(ruta_datos):
        ruta_archivo = os.path.join(ruta_datos, f'{carpeta}')
        for archivo in os.listdir(ruta_archivo):
            ruta_lectura = os.path.join(ruta_archivo, f'{archivo}')
            carpeta_filtrado = os.path.join(ruta_archivo, 'filtrado/')
            try:
                table = load_phones(ruta_lectura)
                table = delete_rows_with_no_phones(table)
                table = filter(table, driver)    
                table.to_excel(str(carpeta_filtrado + archivo.replace(".xlsx", "-filtrado.xlsx")))    
                print(archivo + ' listo.')
            except Exception as e:
                print(archivo + ' --> No se pudo procesar')
                print(e)
                pass
    driver.close()
    return 1 


if __name__ == '__main__':
    main() 