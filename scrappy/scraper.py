from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time, xlsxwriter, os, textwrap, argparse, platform, sys, phonenumbers, pycountry
from playsound import playsound

# Variables globales
COUNTRY = None
CATEGORY = None
LIST = None
OUTPUT = None
OS = None
ACTION_KEY = Keys.COMMAND if OS == 'Mac' else Keys.CONTROL
INDICE = 0

def search_city(name, driver, worksheet):
    '''
    Esta funcion es la que hace el verdadero scraping ...
    '''
    global INDICE
    # Cargo la ciudad
    # Encuentra el cuadro de búsqueda
    search_box = driver.find_element('id', 'searchboxinput')
    # Eliminamos el contenido del cuadro de busqueda
    search_box.send_keys(ACTION_KEY + "a")
    time.sleep(0.8)
    search_box.send_keys(Keys.DELETE)
    time.sleep(0.8)
    # Buscamos el nombre de la ciudad 
    search_box.send_keys(f'{name} {COUNTRY}')  
    time.sleep(0.8)
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)
    # Buscamos el rubro
    search_box.send_keys(ACTION_KEY + "a")
    time.sleep(1)
    search_box.send_keys(Keys.DELETE)
    time.sleep(1)
    search_box.send_keys(CATEGORY)  
    search_box.send_keys(Keys.ENTER)

    time.sleep(3)
                                                   
    listaEmpresas = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
    
    ActionChains(driver).click(listaEmpresas)

    print(f'\n     * Buscando empresas en {name}...')
    for i in range(0, 80):
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
            print(f'     * Se detectaron {a} locales.') 
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
        worksheet.write(INDICE+1, 0, str(a))
        worksheet.write(INDICE+1, 1, str(nombre))
        worksheet.write(INDICE+1, 2, str(servicio))
        worksheet.write(INDICE+1, 3, str(telefono))
        worksheet.write(INDICE+1, 4, str(web))
        worksheet.write(INDICE+1, 5, str(direccion))
        worksheet.write(INDICE+1, 6, str(name))
        INDICE += 1
        a += 1
    print(f'     * Se encontraron {a} empresas en {name} {COUNTRY}')

def load_cities():
    '''
    Lee las ciudades dentro de la lista de ciudades
    '''
    print(' --> Cargando lista de ciudades')
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
    print(' --> Creando driver para el navegador')
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
    print(' --> Comienza la busqueda en maps :D')
    # Buscamos la pagina de google maps
    driver.get('https://www.google.com/maps')
    # Le damos un delay para que cargue la info
    time.sleep(1)
    filename = f'{CATEGORY}_{COUNTRY}_raw_data.xlsx'
    # creamos el archivo xlsx
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Primera Pagina')
    worksheet.write(0,0,'#')
    worksheet.write(0,1,'Nombre')
    worksheet.write(0,2,'Servicio')
    worksheet.write(0,3,'Telefono')
    worksheet.write(0,4,'Web')
    worksheet.write(0,5,'Direccion')
    worksheet.write(0,6,'Ciudad')
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
    print(' --> Filtrando telefonos')
    data = pd.read_excel(workbook_name)
    data = data[~data['Telefono'].astype(str).str.contains('#')]
    data = data[~data['Telefono'].astype(str).str.contains('[a-zA-Z]')]
    data = data.drop_duplicates(subset='Telefono')
    data.to_excel(f'{CATEGORY}_{COUNTRY}_contactos_con_telefono.xlsx')
    return f'{CATEGORY}_{COUNTRY}_contactos_con_telefono.xlsx'

def phone_nationality_filter(workbook_name):
    
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
    print(f' --> Filtrando telefonos pertenecientes a {COUNTRY}')
        
    data = pd.read_excel(workbook_name)
    data['Telefono'] = data['Telefono'].astype(str)
    for i, valor in enumerate(data['Telefono']):
        if not check(valor):
            data.drop(i, axis=0, inplace=True)

    data.to_excel(f'{CATEGORY}_{COUNTRY}_contactos_nacionales_con_telefono.xlsx', index=False)

    return f'{CATEGORY}_{COUNTRY}_contactos_nacionales_con_telefono.xlsx'


def existe_en_whatsapp(phone, driver):
    input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[1]/div/div/div[2]/input')
    time.sleep(0.5)
    input.send_keys(phone)
    time.sleep(4.5) 
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[2]/div[2]/div[2]')
        input.send_keys(ACTION_KEY + "a")
        time.sleep(0.5)
        input.send_keys(Keys.DELETE)
        return True
    except:
        input.send_keys(ACTION_KEY + "a")
        time.sleep(0.5)
        input.send_keys(Keys.DELETE)
        return False
        
# 30 segundos para iniciar sesion
def open_whatsapp(driver):
    print(f' --> Abriendo Whatsapp')
    driver.get('https://web.whatsapp.com/')
    time.sleep(30)
    three_dots = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div/span')
    three_dots.click()
    time.sleep(2)
    new_group = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/span/div/ul/li[1]/div')
    new_group.click()
    time.sleep(2)

def filter(filename, driver):
    def convertir_segundos_a_hora(segundos):
        # Dividir los segundos en horas, minutos y segundos
        segundos_entero = int(segundos)
        # Dividir los segundos en horas, minutos y segundos
        horas, segundos_entero = divmod(segundos_entero, 3600)
        minutos, segundos_entero = divmod(segundos_entero, 60)

        # Formatear la hora en formato HH:MM:SS
        hora_formateada = "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos_entero)    
        return hora_formateada

    print(' --> Filtrando telefonos que existan en Whatsapp')
    table = pd.read_excel(filename)
    aprox_time = convertir_segundos_a_hora(len(table)*(4.5))
    print(f' Este proceso tardara aproximadamente: {aprox_time}')
    for index, row in table.iterrows():
        phone = row['Telefono']
        if not existe_en_whatsapp(phone, driver):
            table = table.drop(index)

    
    table.to_excel(f'{CATEGORY}_{COUNTRY}_prospectos.xlsx')
    return

def reproducir_alarma_continuamente(ruta_archivo):
    reproduciendo = True

    # Función que se ejecuta para detener la reproducción
    def detener_reproduccion():
        nonlocal reproduciendo
        input("Presiona Enter para detener la alarma...")
        print('''
              ###############################################
              ##                                           ##
              ##      ESCANEE EL QR PARA ABRIR SU          ##
              ##      CUENTA DE WHATSAPP                   ##
              ##                                           ##
              ###############################################
              ''')
        reproduciendo = False

    # Reproducir la alarma en un bucle hasta que se presione Enter
    while reproduciendo:
        playsound(ruta_archivo)
        detener_reproduccion()
    # Llama a la función para detener la reproducción

def generar_stats():
    print(' --> Generando estadisticas')
    # Nombres de los archivos Excel
    nombres_archivos = [
        f'{CATEGORY}_{COUNTRY}_raw_data.xlsx',
        f'{CATEGORY}_{COUNTRY}_contactos_con_telefono.xlsx',
        f'{CATEGORY}_{COUNTRY}_contactos_nacionales_con_telefono.xlsx',
        f'{CATEGORY}_{COUNTRY}_prospectos.xlsx'
    ]
    
    # Lista para almacenar la cantidad de líneas de cada archivo
    cantidad_lineas = []

    # Iterar sobre los archivos Excel
    for nombre_archivo in nombres_archivos:
        # Cargar el archivo Excel en un DataFrame
        df = pd.read_excel(nombre_archivo)
        # Contar la cantidad de líneas y almacenarla en la lista
        cantidad_lineas.append(len(df))

    # Calcular el porcentaje de líneas del archivo prospectos respecto a raw_data
    porcentaje = (cantidad_lineas[3] / cantidad_lineas[0]) * 100

    # Crear un texto con la información de las líneas y el porcentaje
    texto = ""
    for nombre_archivo, cantidad in zip(nombres_archivos, cantidad_lineas):
        texto += f"Archivo: \t{nombre_archivo} \nDatos: \t\t{cantidad}\n ################# \n"
        
    # Agregar la información del porcentaje al texto
    texto += f"\n\nSolo el {porcentaje:.2f}% de empresas encontradas son posibles prospectos"

    # Guardar la información en un archivo de texto
    with open(f'{CATEGORY}_{COUNTRY}_estadisticas.txt', 'w') as archivo_texto:
        archivo_texto.write(texto)    

def main():
    driver = create_driver()
    cities = load_cities()
    # Generacion de data sin procesar
    workbook_name_raw_data = scrap_maps(cities, driver)
    # Filtro de telefonos
    workbook_name_phone_filter = phone_filter(workbook_name_raw_data)
    # Filtro de telefonos nacionales
    workbook_name_phone_nationality_filter = phone_nationality_filter(workbook_name_phone_filter)
    # Filtro de prospectos
    reproducir_alarma_continuamente('../assets/alarm.mp3')
    #workbook_name_phone_nationality_filter = 'taxi_Mexico_contactos_nacionales_con_telefono.xlsx'
    open_whatsapp(driver)
    filter(workbook_name_phone_nationality_filter, driver)                        
    driver.close()
    generar_stats()
    print('\n\nGracias por usar scrappy-bot!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='''
         ___  ___ _ __ __ _ _ __  _ __  _   _ 
        / __|/ __| '__/ _` | '_ \| '_ \| | | |
        \__ \ (__| | | (_| | |_) | |_) | |_| |
        |___/\___|_|  \__,_| .__/| .__/ \__, |
                           | |   | |     __/ |
                           |_|   |_|    |___/ 

            v0.1 @sleepydogo
    ''',
    formatter_class=argparse.RawDescriptionHelpFormatter, 
    epilog=textwrap.dedent('''Example:
        bot.py -c Bolivia -cat Hoteles -l lista.txt 
        bot.py -c Paraguay -cat Taxi -l lista_paraguay.txt 
    '''))
    parser.add_argument('-c', '--country', required=False, type=str, help='sets the country to look into')
    parser.add_argument('-cat', '--category', required=True, type=str, help='sets the category of stores/places that we are gonna look for')
    parser.add_argument('-l', '--list', required=True, type=str, help='cities list filename')
    
    args = parser.parse_args()

    if args.country == None:
        COUNTRY = ' '
    else:
        COUNTRY = args.country
    
    CATEGORY = args.category
    LIST = args.list
    
    main()
    

