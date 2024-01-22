from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import time, xlsxwriter
import os

def extraerInformacionDeUrl(url, browser, worksheet, index):

    browser.get(url)
    time.sleep(2)
    try:
        nombre =  browser.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1').text
    except:
        pass
    try: 
        telefono = browser.find_element(By.CSS_SELECTOR, 'div.RcCsl:nth-child(8) > button:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)').text
    except:                                               
        telefono = 'No tiene...'                          
    try:
        web = browser.find_element(By.CSS_SELECTOR, '.ITvuef > div:nth-child(1)').text
    except:
        web = 'No tiene...'
    try:                                      
        menu = browser.find_element(By.CSS_SELECTOR, 'a.CsEnBe > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)').text
    except:
        menu = 'No tiene...'
    try:                                            
        direccion = browser.find_element(By.CSS_SELECTOR, 'div.RcCsl:nth-child(3) > button:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)').text
    except: 
        direccion = 'No tiene...'
    print('------------------------------')
    print('     * Se encontro: --> ')
    print(str(nombre) +'\n' + str(telefono)+'\n' + str(web)+'\n' + str(menu)+'\n' + str(direccion)+ '\n')            

    worksheet.write(index+1, 0, str(index))
    worksheet.write(index+1, 1, str(nombre))
    worksheet.write(index+1, 2, str(url))
    worksheet.write(index+1, 3, str(direccion))
    worksheet.write(index+1, 4, str(telefono))
    worksheet.write(index+1, 5, str(web))
    worksheet.write(index+1, 6, str(menu))


    print('\n     * Se almaceno correctamente ' + str(nombre) + '.')


def searchCity(name, driver, worksheet):
    # Cargo la ciudad
    # Encuentra el cuadro de búsqueda
    search_box = driver.find_element('id', 'searchboxinput')
    search_box.send_keys(Keys.COMMAND + "a")
    time.sleep(0.8)
    search_box.send_keys(Keys.DELETE)
    time.sleep(0.8)
    search_box.send_keys(name)  # Ingresa la ubicación que deseas buscar
    # Presiona la tecla Enter para realizar la búsqueda
    time.sleep(0.8)
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)

    rubro = 'taxi'
    
    search_box.send_keys(Keys.COMMAND + "a")
    time.sleep(1)
    search_box.send_keys(Keys.DELETE)
    time.sleep(1)
    search_box.send_keys(rubro)  # Ingresa la ubicación que deseas buscar
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
        # telefono
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
        
def loadCityList(nombre_archivo):
    # Inicializar un array para almacenar las líneas
    lineas = []

    # Abrir el archivo y leer línea por línea
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            # Eliminar caracteres de nueva línea y agregar la línea al array
            lineas.append(linea.strip())
    return lineas

def main():

    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"

    # Elimina la línea que especifica el ejecutable_path
    # chrome_driver_binary = "/usr/local/bin/chromedriver"

    # Utiliza ChromeDriverManager para gestionar automáticamente la versión del controlador de Chrome
    driver = webdriver.Chrome(options=options)


    driver.get('https://www.google.com/maps')
    time.sleep(1)
    print(''''
                _..._
              .'     '.      _
             /    .-""-\   _/ \ Bienvenido al espacio
           .-|   /:.   |  |   | exterior
           |  \  |:.   /.-'-./
           | .-'-;:__.'    =/
           .'=  *=|NASA _.='
          /   _.  |    ;
         ;-.-'|    \   |
        /   | \    _\  _\\
        \__/'._;.  ==' ==\\
                 \    \   |
                 /    /   /
                 /-._/-._/
                 \   `\  \\
                  `-._/._/
    \n' ''')
    
    # Obtener la ruta actual
    ruta_actual = os.getcwd()

    # Combinar la ruta actual con la carpeta "ciudades"
    ruta_ciudades = os.path.join(ruta_actual, "listas-ciudades")
    for archivo in os.listdir(ruta_ciudades):
        nombre = 'listas-ciudades/' + archivo
    
        cities = loadCityList(nombre)

        for city in cities:
            namefile = city + ".xlsx"
            name = city 
            ruta = os.path.join(os.getcwd(), f'datos//{namefile}')
            workbook = xlsxwriter.Workbook(ruta)
            worksheet = workbook.add_worksheet('Primera Pagina')
            worksheet.write(0,0,'#')
            worksheet.write(0,1,'Nombre')
            worksheet.write(0,2,'Servicio')
            worksheet.write(0,3,'Telefono')
            worksheet.write(0,4,'Web')
            worksheet.write(0,5,'Direccion')

            searchCity(name, driver, worksheet)
            workbook.close()
            print('\n\n     --> Se ha guardado correctamente ' + namefile)            

    driver.close()

if __name__ == '__main__':
    main()
