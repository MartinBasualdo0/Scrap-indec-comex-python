import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from glob import glob
import time
import zipfile
from typing import Literal


def init_driver():
    carpeta_descarga=os.getcwd()+"\\downloads"
    service = Service(ChromeDriverManager().install())
    #Con getcwd() se encuentra el path absoluto
        
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : carpeta_descarga,
            "directory_upgrade": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(service=service,options=chrome_options)
    return driver

def every_downloads_chrome(driver):
    '''
    Verifica cuando terminan las descargas.
    '''
    # Ir a la página de descargas de Chrome
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    
    # Ejecutar script para obtener los items descargados
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

def scrap_database(anio_desde:str, anio_hasta:str, frecuencia = Literal["mensual","anual"]):
    '''
    Descarga la base de datos de comercio exterior según los años y frecuencia especificados.
    
    frecuencia: Mensual o Anual (por defecto Mensual)
    '''
    
    driver = init_driver()
    frecuencia = frecuencia.capitalize()
    link_consulta='https://comex.indec.gob.ar/?_ga=2.1947448.887743671.1661390997-1687177890.1630124319#/database'
    driver.get(link_consulta)
    
    # Wait for the page to be fully loaded
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    
    # Obtener elementos de la página
    lista_botones = driver.find_elements(By.CLASS_NAME, "form-control")
    
    # Seleccionar el tipo de comercio (exportaciones)
    select_comercio = Select(lista_botones[0])
    select_comercio.select_by_value('imports')
    
    # Seleccionar la frecuencia
    select_frecuencia = Select(lista_botones[2])
    select_frecuencia.select_by_visible_text(frecuencia)
    
    # Seleccionar el año
    select_anio = Select(lista_botones[1])
    opciones_anio=[]
    for option in select_anio.options: 
        opciones_anio.append(option.get_attribute('value'))
    opciones_anio.pop(0)

    opciones_anio=list(filter(lambda x: x>=anio_desde and x<=anio_hasta,opciones_anio))
    # Descargar los datos
    for opcion in opciones_anio:
        select_anio.select_by_visible_text(opcion)
        descarga = driver.find_element(By.CLASS_NAME, "btn-outline-primary")
        descarga.click()
        time.sleep(1)
    
    return opciones_anio


def extraer_y_concatenar_dfs_anuales(opciones, anio_hasta):
    '''Extrae y concatena las dfs anuales'''
    columnas_anuales = ['Año', 'NCM', 'Pdes', 'Pnet(kg)', 'FOB(u$s)']
    dfs = {}
    for idx, opcion in enumerate(opciones):
        with zipfile.ZipFile(f'./downloads/imports_{opcion}_Y.zip', 'r') as zip_ref:
            zip_ref.extractall('./downloads')
        try:
            df = pd.read_csv(f'./downloads/impoa{opcion[2:]}.csv', sep=';', encoding='latin-1', decimal=',',
                             dtype={'NCM': str, 'Porg': str, 'Año':str})
        except:
            df = pd.read_csv(f'./downloads/expot{opcion[2:]}.csv', sep=';', encoding='latin-1', decimal=',',
                             dtype={'NCM': str, 'pdes': str})
        df = df.rename(columns={col: col.lower() for col in df.columns})
        # df.ncm = df.ncm.apply(lambda x: x.strip())
        dfs[str(int(anio_hasta) - idx)] = df
        eliminar = input('Eliminar descargas? Enter/Sí para si')
        if eliminar[0].lower()=="s":
            for i in glob("./downloads/*", recursive = True): os.remove(i)
    return pd.concat([dfs[key] for key in dfs.keys()])

def extraer_y_concatenar_dfs_mensuales(opciones, anio_hasta):
    '''Extrae y concatena las dfs mensuales'''
    columnas = ['Año', 'Mes', 'NCM', 'Pdes', 'Pnet(kg)', 'FOB(u$s)', 'CIF(u$s)']
    dfs = {}
    for idx, opcion in enumerate(opciones):
        with zipfile.ZipFile(f'./downloads/exports_{opcion}_M.zip', 'r') as zip_ref:
            zip_ref.extractall('./downloads')
        try:
            df = pd.read_csv(f'./downloads/exponm{opcion[2:]}.csv', sep=';', encoding='latin-1', decimal=',',
                             dtype={'NCM': str, 'pdes': str})
        except:
            df = pd.read_csv(f'./downloads/expom{opcion[2:]}.csv', sep=';', encoding='latin-1', decimal=',',
                             dtype={'NCM': str, 'pdes': str})
        # df = df.rename(columns={col: col.lower() for col in columnas})
        df.ncm = df.ncm.apply(lambda x: x.strip())
        dfs[str(int(anio_hasta)-idx)] = df
    return pd.concat([dfs[key] for key in dfs.keys()])

def limpiar_y_corregir_df(df):
    # Convertir columna "pnet(kg)" a string y reemplazar "," por "."
    df['pnet(kg)'] = df['pnet(kg)'].astype(str).apply(lambda x: x.replace(',', '.'))
    # Convertir columna "fob(u$s)" a string y reemplazar "," por "."
    df['fob(u$s)'] = df['fob(u$s)'].astype(str).apply(lambda x: x.replace(',', '.'))
    # Reemplazar valores que contengan "s" en "pnet(kg)" por "0"
    df.loc[df['pnet(kg)'].str.contains("s"), 'pnet(kg)'] = "0"
    # Reemplazar valores que contengan "s" en "fob(u$s)" por "0"
    df.loc[df['fob(u$s)'].str.contains("s"), 'fob(u$s)'] = "0"
    # Convertir columna "pnet(kg)" a float
    df['pnet(kg)'] = df['pnet(kg)'].astype(float)
    # Convertir columna "fob(u$s)" a float
    df['fob(u$s)'] = df['fob(u$s)'].astype(float)
    # Convertir columna "pdes" a string
    df['pdes'] = df['pdes'].astype(str)
    # Convertir columna "año" a string
    df['año'] = df['año'].astype(str)
    return df


    


def scrap_base_indec(anio_desde, anio_hasta, frecuencia):
    driver = init_driver

    opciones = scrap_database(anio_desde=anio_desde, anio_hasta=anio_hasta,frecuencia="mensual")
    scrap_database(anio_desde=anio_desde,anio_hasta=anio_hasta, frecuencia="anual")

    paths = WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
    driver.quit()

    df_mensual = extraer_y_concatenar_dfs_mensuales(opciones = opciones, anio_hasta = anio_hasta)
    df_anual = extraer_y_concatenar_dfs_anuales(opciones = opciones, anio_hasta=anio_hasta)
    if frecuencia[0].lower() == "m":
        return df_mensual
    elif frecuencia[0].lower() == "a":
        return df_anual




