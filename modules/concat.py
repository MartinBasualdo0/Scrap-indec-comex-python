import pandas as pd
import zipfile
from typing import Literal
from glob import glob
from modules.constants import DF_COLUMNS

def concat_dfs(years:list[int], commerce:Literal["imports","exports"], frequency:Literal["Y","M"]):
    '''Extracts and concats dfs'''
    dfs=[]
    if frequency == "Y":
        columns = [item for item in DF_COLUMNS if item != 'month']
    else:
        columns = DF_COLUMNS
    for year in years:
        with zipfile.ZipFile(f'./downloads/{commerce}_{year}_{frequency}.zip', 'r') as zip_ref:
            zip_ref.extractall('./downloads')
        if commerce == "imports":
            df=pd.read_csv(glob(f'./downloads/impo*{str(year)[2:]}.csv')[0], sep=';', encoding='latin-1',decimal=',')
        else:
            try: df=pd.read_csv(glob(f'./downloads/expon*{str(year)[2:]}.csv')[0], sep=';', encoding='latin-1',decimal=',')
            except: df=pd.read_csv(glob(f'./downloads/expo*{str(year)[2:]}.csv')[0], sep=';', encoding='latin-1',decimal=',')
        df.columns = columns[:len(df.columns)]
        df.ncmCode=df.ncmCode.astype(str)\
            .apply(lambda x: x.strip())\
                .apply(lambda x: x.zfill(8))
        df.countryCode = df.countryCode.astype(str)\
            .apply(lambda x: x.zfill(3))
        df.year = df.year.astype(str)
        if frequency == "M":
            df.month = df.month.astype(str).apply(lambda x: x.zfill(2))
        # dfs[str(2022-idx)] = df
        dfs.append(df)
    df = pd.concat(dfs)
    if frequency == "M":
        df.sort_values(["year", "month"], ascending=True)
    else:
        df.sort_values("year", ascending=True)
    return pd.concat(dfs)