
# Cargar lista de ciudades de un pais
# 1. Cargar lista de ciudades
# 2. Buscar la ciudad en google maps
# 3. Buscar la compania en la ciudad
# 4. Guardar en una hoja de datos los datos de la tienda: nombre, ciudad, pais, servicio, telefono, web
#       Si no tiene numero de telefono no la guardo
# 5. Recorrer esa lista de datos y filtrar los que tienen whatsapp 
# 6. Repetir
# 
# Variables: Pais, 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import time, xlsxwriter, os, platform, argparse, textwrap


# Variables de ejecutable
MAC_OS_PATH = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'
LINUX_OS_PATH = '/usr/bin/google-chrome'
CHROME_DRIVER_PATH = ''
# Variables de almacenamiento
RUTA_ACTUAL = None
# Argumentos
CATEGORIA = None
LISTA_CIUDADES = None
LISTA_TELEFONOS = None
RUBRO = None


def loadVariables():
    '''
        Esta funcion determina en que plataforma se esta ejecutando el script.
    '''
    sistema_operativo = platform.system()
    if sistema_operativo == "Linux":
        CHROME_DRIVER_PATH = LINUX_OS_PATH
    elif sistema_operativo == "Darwin":
        CHROME_DRIVER_PATH = MAC_OS_PATH
    else:
        print('Windows es para petes..')

    RUTA_ACTUAL = os.getcwd()

def loadDriver():
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = CHROME_DRIVER_PATH
    driver = webdriver.Chrome(options=options)
    return driver



def main():
    # loadVariables()
    # driver = loadDriver()
    parser = argparse.ArgumentParser(
    description='''
                 _                                  _               _           _                 
  ___ ___   ___ | |  ___  ___ _ __ __ _ _ __  _ __ (_)_ __   __ _  | |__   ___ | |_     _   _ __  
 / __/ _ \ / _ \| | / __|/ __| '__/ _` | '_ \| '_ \| | '_ \ / _` | | '_ \ / _ \| __|   (_) | '_ \ 
| (_| (_) | (_) | | \__ \ (__| | | (_| | |_) | |_) | | | | | (_| | | |_) | (_) | |_     _  | |_) |
 \___\___/ \___/|_| |___/\___|_|  \__,_| .__/| .__/|_|_| |_|\__, | |_.__/ \___/ \__|   (_) | .__/ 
                                       |_|   |_|            |___/                          |_|    

        author: sleepydogo
    ''',
    formatter_class=argparse.RawDescriptionHelpFormatter, 
    epilog=textwrap.dedent('''Example
        bot.py -m -c hotel -cl cities.txt -s hotels-northern-canada
        bot.py -m -c hotel -cl cities.txt 
        bot.py -w -tl phones.txt -s phones-hotels-northenr-canada                   
    '''))
    parser.add_argument('-m', '--maps', action='store_true', help='uses the maps bot')
    parser.add_argument('-w', '--whatsapp', action='store_true', help='uses the whatsapp bot')
    parser.add_argument('-b', '--both', action='store_true', help='uses both bot')
    parser.add_argument('-c', '--category', type=str, action='store', help='specifies stores you are looking for, only for maps bot')
    parser.add_argument('-cl', '--cities', type=str, action='store', help='cities list filename, only for maps bot')
    parser.add_argument('-tl', '--telephone', type=str, action='store', help='telephones list filename, only for whatsapp bot')
    parser.add_argument('-s', '--store', type=str, action='store', help='folder filename to store the data')
    args = parser.parse_args()
    
    if args.cities:
        print('cities')


if __name__ == '__main__':
    main()
    