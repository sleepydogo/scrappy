from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time, xlsxwriter, os, textwrap, argparse, platform, sys, phonenumbers, pycountry

# Variables globales
COUNTRY = None
CATEGORY = None
LIST = None
OUTPUT = None
OS = None

def search_city(name, driver, worksheet):
    '''
    Esta funcion es la que hace el verdadero scraping ...
    '''

    action_key = Keys.COMMAND if OS == 'Mac' else Keys.CONTROL

    # Cargo la ciudad
    # Encuentra el cuadro de búsqueda
    search_box = driver.find_element('id', 'searchboxinput')
    search_box.send_keys(action_key + "a")
    time.sleep(0.8)
    search_box.send_keys(Keys.DELETE)
    time.sleep(0.8)
    search_box.send_keys(name)  # Ingresa la ubicación que deseas buscar
    # Presiona la tecla Enter para realizar la búsqueda
    time.sleep(0.8)
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)
    
    search_box.send_keys(action_key + "a")
    time.sleep(1)
    search_box.send_keys(Keys.DELETE)
    time.sleep(1)
    search_box.send_keys(CATEGORY)  # Ingresa la ubicación que deseas buscar
    # Presiona la tecla Enter para realizar la
    search_box.send_keys(Keys.ENTER)

    time.sleep(3)
                                                   
    listaEmpresas = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
    
    ActionChains(driver).click(listaEmpresas)

    print('\n\n     * Buscando empresas...')
    for i in range(0, 100):
        try:
            listaEmpresas.send_keys(Keys.PAGE_DOWN)
        except:
            print(f'{name} --> Error al procesar la ciudad.')
            return
        if ((i%7) == 0):
            time.sleep(0.7)

    a = 0
    for i in range(3, 501, 2):
        # nombre de la empresa
        try: 
            nombre =  driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/div[2]').text
        except NoSuchElementException:
            print('\n\n\n     * Se detectaron ' + str(a) + ' locales.') 
            return 
        # telefono
        try: 
            telefono = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[2]/span/span').text
        except:                                               
            telefono = None                  
        
        if telefono == None: 
            try: 
                telefono = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[2]/span[2]/span[2]').text
            except:                                               
                telefono = '#########'     
        try:
            web = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[2]/div[1]/a').get_attribute("href")

        except:
            web = '-'
        try:                                            
            direccion = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[2]/span[2]').text
        except: 
            direccion = '-'
        try:                                            
            servicio = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div['+str(i)+']/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[1]/span').text
        except: 
            servicio = '-'
        print(f'     * Se encontro: --> {a} {nombre} {telefono} {direccion} {servicio} {web}')
        worksheet.write(a+1, 0, str(a))
        worksheet.write(a+1, 1, str(nombre))
        worksheet.write(a+1, 2, str(servicio))
        worksheet.write(a+1, 3, str(telefono))
        worksheet.write(a+1, 4, str(web))
        worksheet.write(a+1, 5, str(direccion))
        a += 1

def load_cities():
    '''
    Lee las ciudades dentro de la lista de ciudades
    '''
    # Inicializar un array para almacenar las líneas
    lineas = []
    # Abrir el archivo y leer línea por línea
    with open(LIST, "r") as archivo:
        for linea in archivo:
            # Eliminar caracteres de nueva línea y agregar la línea al array
            lineas.append(linea.strip())
    return lineas

def create_driver():
    '''
    Esta funcion retorna el driver de selenium basado en el OS del usuario
    '''
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    sistema_operativo = platform.system()
    if sistema_operativo == "Linux":
        CHROME_DRIVER_PATH = '/usr/bin/google-chrome'
    elif sistema_operativo == "Darwin":
        OS = 'Mac'
        CHROME_DRIVER_PATH = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'
    else:
        sys.exit('No funciona en windows...')
    options.binary_location = CHROME_DRIVER_PATH
    driver = webdriver.Chrome(options=options)
    time.sleep(4)
    return driver

def scrap_maps(cities, driver):
    '''
    Esta funcion scrapea maps, almacenando todo lo que encuentra en un archivo 
    llamado 'raw_data_COUNTRY.xlsx'
    '''
    # Buscamos la pagina de google maps
    driver.get('https://www.google.com/maps')
    # Le damos un delay para que cargue la info
    time.sleep(1)
    filename = f'raw_data_{COUNTRY}.xlsx'
    # creamos el archivo xlsx
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Primera Pagina')
    worksheet.write(0,0,'#')
    worksheet.write(0,1,'Nombre')
    worksheet.write(0,2,'Servicio')
    worksheet.write(0,3,'Telefono')
    worksheet.write(0,4,'Web')
    worksheet.write(0,5,'Direccion')
    # Scrapeamos maps y almacenamos cada resultado en una fila del dataset
    for city in cities:
        search_city(city, driver, worksheet)
    # Lo guardamos
    workbook.close()
    # Volvemos a leerlo y descartamos duplicados
    # TODO: Mejorar esta parte
    df = pd.read_excel(filename)
    df = df.drop_duplicates()
    df.to_excel(filename)
    return filename


def phone_filter(workbook_name):
    '''
    Esta funcion toma como entrada el nombre de un excel y lo filtra
    dejando solo aquellas filas que contengan un numero de telefono valido
    '''
    data = pd.read_excel(workbook_name)
    data = data[~data['Telefono'].astype(str).str.contains('#')]
    data = data[~data['Telefono'].astype(str).str.contains('[a-zA-Z]')]
    data.to_excel(f'contactos_con_telefono_{COUNTRY}.xlsx')
    return data

def phone_nationality_filter(data):
    
    def check(numero_telefono):
        try:
            pais = pycountry.countries.search_fuzzy(COUNTRY)
            abreviacion = pais[0].alpha_2
            # Parsear el número de teléfono
            numero_parsed = phonenumbers.parse(numero_telefono, abreviacion)
            # Verificar si el número es válido y si pertenece a Paraguay
            return phonenumbers.is_valid_number(numero_parsed) and phonenumbers.region_code_for_number(numero_parsed) == abreviacion
        except phonenumbers.NumberParseException:
            # Manejar excepciones si el número no se puede analizar
            return False
        
    data['Telefono'] = data['Telefono'].astype(str)
    for indice, valor in enumerate(data['Telefono']):
        if not check(valor):
            data = data.drop(indice)

    data.to_excel(f'contactos_nacionales_con_telefono_{COUNTRY}.xlsx', index=False)

    return data


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

def filter(table, driver):
    for index, row in table.iterrows():
        phone = row['Telefono']
        if not existe_en_whatsapp(phone, driver):
            table = table.drop(index)
            print(phone)
        else:
            print(phone + '---> ok')
    table.to_excel(f'prospectos_{COUNTRY}.xlsx')
    return


def main():
    driver = create_driver()
    cities = load_cities()
    # Generacion de data sin procesar
    workbook_name = scrap_maps(cities, driver)
    # Filtro de telefonos
    data = phone_filter(workbook_name)
    # Filtro de telefonos nacionales
    data = phone_nationality_filter(data)
    # Filtro de prospectos
    open_whatsapp(driver)
    data = filter(data, driver)                        

    driver.close()

if __name__ == '__main__':
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
    epilog=textwrap.dedent('''Example:
        bot.py -c Bolivia -cat Hoteles -l lista.txt -o Bolivia 
        bot.py -c Paraguay -cat Taxi -l lista_paraguay.txt -o Paraguay_taxis 
    '''))
    parser.add_argument('-c', '--country', required=True, type=str, help='sets the country to look into')
    parser.add_argument('-cat', '--category', required=True, type=str, help='sets the category of stores/places that we are gonna look for')
    parser.add_argument('-l', '--list', required=True, type=str, help='cities list filename')
    parser.add_argument('-o', '--output', default='output' ,help='output files name')
    
    args = parser.parse_args()

    COUNTRY = args.country
    CATEGORY = args.category
    LIST = args.list
    OUTPUT = args.output
    
    main()
    

