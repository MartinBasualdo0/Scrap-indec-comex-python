import requests
from typing import Literal
import re
import os
from modules.check import check_and_create_directories

def _get_zip_names(commerce:Literal["exports", "imports", "all"], 
                  frequency: Literal["Y", "M", "all"],
                  year_from:int = None):
    api_url = 'https://comexbe.indec.gob.ar/public-api/staticData'
    response = requests.get(api_url)
    data = response.json()
    zip_file_info = data['zipFiles']
    id_values = [item['_id'] for item in zip_file_info]
    if commerce != "all":
        id_values = [value for value in id_values if value.startswith(commerce)]
    if frequency != "all":
        id_values = [value for value in id_values if value[-5] == frequency]
    if year_from:
        id_values = [value for value in id_values if int(re.findall(r'\d+', value)[0]) >= year_from]
    return id_values

def _download_zips(zip_names:list[str], folder_path:str ):
    for zip_name in zip_names:
        url = f'https://comex.indec.gob.ar/files/zips/{zip_name}'

        # The headers from your proxy intercept, including cookies
        headers = {
            'Cookie': '_ga=GA1.3.713773624.1711596853; _gid=GA1.3.164217743.1711596853; cookiesession1=678A3F785F8ACD48A93F935EA37EB83A',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-419,es;q=0.9',
            'Priority': 'u=4, i',
            'Connection': 'close'
        }

        # Make the GET request to download the file
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in write-binary mode and write the content
            with open(f'{folder_path}/{zip_name}', 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully. {zip_name}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    
def _delete_all_files_in_folder(folder_path):
    # Ensure the folder path ends with a slash
    if not folder_path.endswith('/'):
        folder_path += '/'
    
    # Loop through all the contents of the folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = folder_path + filename
        
        # Check if the item is a file
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)
    
def main_download_zips(
    commerce:Literal["exports", "imports", "all"], 
    frequency: Literal["Y", "M", "all"],
    year_from:int = None,
    drop_all_files:bool = True,
    ):
    check_and_create_directories()
    download_folder = "./downloads"
    if drop_all_files:
        _delete_all_files_in_folder(download_folder)
    zip_names = _get_zip_names(commerce, frequency, year_from)
    _download_zips(zip_names, download_folder)
    
def get_years_from_filenames(folder_path):
    if not folder_path.endswith('/'):
        folder_path += '/'
    years = []
    for filename in os.listdir(folder_path):
        year_match = re.findall(r'\d{4}', filename)
        if year_match:
            years.append(int(year_match[0]))
    return years