# Este filtro elimina todos aquellos contactos que no posean numero de telefonos
# asociados y aquellas planillas de datos que no posean contactos.

import pandas as pd
import os

def load_phones(filename):
    data = pd.read_excel(filename)
    # Eliminamos la primera columna de indices
    data = data.iloc[:, 1:]
    return data

def delete_rows_with_no_phones(data):
    data = data[~data['Telefono'].astype(str).str.contains('#')]
    data = data[~data['Telefono'].astype(str).str.contains('[a-zA-Z]')]
    return data

#def main():
#    ruta_datos = os.path.join(os.getcwd(), "datos2") 
#    ## Para cada carpeta dentro de "datos2"
#    for carpeta in os.listdir(ruta_datos):
#        ruta_carpeta = os.path.join(ruta_datos, f'{carpeta}')
#        # Creo una carpeta dentro de la carpeta del pais que se llame "filtro-1"
#        ruta_archivos_filtrados = os.path.join(ruta_carpeta, 'filtro-1')
#        if not os.path.exists(ruta_archivos_filtrados):
#            os.makedirs(ruta_archivos_filtrados)
#        # Para cada carpeta de pais
#        for archivo in os.listdir(ruta_carpeta):
#            # Creo la ruta para el archivo .xslx
#            ruta_archivo = os.path.join(ruta_carpeta, f'{archivo}')
#            # Si la ruta no corresponde a una carpeta
#            if not os.path.isdir(ruta_archivo):
#                # Cargo el dataset y lo filtro
#                dataset = load_phones(ruta_archivo)
#                dataset = delete_rows_with_no_phones(dataset)
#                if len(dataset) > 1:
#                    # Guardo aquellos que contengan info
#                    dataset.to_excel(os.path.join(ruta_archivos_filtrados, archivo))    
#                    print(f'{archivo} listo!')
#                else:   
#                    print(f'{archivo} eliminado!')
#                    
#    return 0

def main():
    carpeta = 'Paraguay'
    ruta_carpeta = os.path.join(os.getcwd(), f'{carpeta}')
    # Creo una carpeta dentro de la carpeta del pais que se llame "filtro-1"
    ruta_archivos_filtrados = os.path.join(ruta_carpeta, 'filtro-1')
    if not os.path.exists(ruta_archivos_filtrados):
        os.makedirs(ruta_archivos_filtrados)
    # Para cada carpeta de pais
    for archivo in os.listdir(ruta_carpeta):
        print(archivo)
        # Creo la ruta para el archivo .xslx
        ruta_archivo = os.path.join(ruta_carpeta, f'{archivo}')
        # Si la ruta no corresponde a una carpeta
        if not os.path.isdir(ruta_archivo):
            # Cargo el dataset y lo filtro
            dataset = load_phones(ruta_archivo)
            dataset = delete_rows_with_no_phones(dataset)
            if len(dataset) > 1:
                # Guardo aquellos que contengan info
                dataset.to_excel(os.path.join(ruta_archivos_filtrados, archivo))    
                print(f'{archivo} listo!')
            else:   
                print(f'{archivo} eliminado!')
                    
    return 0


if __name__ == '__main__':
    main()