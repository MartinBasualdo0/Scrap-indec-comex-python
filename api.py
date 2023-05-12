#/docs para ver la docu
from fastapi import FastAPI, Path, Query
import pandas as pd

expo_anual = pd.read_csv('./output/expo_anual.csv').to_json(orient="table")
expo_mensual = pd.read_csv('./output/expo_desagregado_ncm_pais.csv').to_json(orient="table")
impo_anual = pd.read_csv('./output/impo_anual.csv').to_json(orient="table")
impo_mensual = pd.read_csv('./output/expo_desagregado_ncm_pais.csv').to_json(orient="table")
#Crear una funcion para filtrar las df

app = FastAPI() #Creo el objeto api

# Creo un endpoint, con un path para la database
# @app.get('/database')
# def database(
#     # comercio: str = Path(None, description="Exportaciones (\"expo\") o importaciones (\"impo\")"), 
#             #  desde: int = Path(None, description= "Desde qué año"),
#             #  ncm: str = Path (None, description = "Nomenclatura buscada (opcional)"), 
#             #  cod_pais: int = Path(None, description = "Codigo del pais buscado (opcional)")
#              ):
#     # if not q:
#         return "Por favor, agregar los parámetros necesarios"
    
@app.get('/database')
def get_data(comercio: str = None,
             freq: str = None,
             desde: int = None,
             ncm: str = None,
             cod_pais: int = None):
    if comercio == 'expo' and freq == 'anual':
        return expo_anual
    if comercio == 'expo' and freq == 'mensual':
        return expo_mensual
    if comercio == 'impo' and freq == 'anual':
        return impo_anual
    if comercio == 'impo' and freq == 'mensual':
        return impo_mensual