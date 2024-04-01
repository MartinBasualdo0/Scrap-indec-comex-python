from typing import Literal
from modules.indec_request import main_download_zips, get_years_from_filenames
from modules.concat import concat_dfs
from modules.custom_secrecy import customs_secrecy_treatment
from modules.joins import insert_country, insert_ncm_description
from modules.constants import MONTH_DICT, TITLES_DICT
from modules.plots import bar_plot

def main_get_commerce_df(
    commerce:Literal["exports", "imports", "all"], 
    frequency: Literal["Y", "M", "all"],
    year_from:int = None,
    drop_all_files:bool = True,
):
    main_download_zips(commerce=commerce, frequency=frequency, year_from=year_from, drop_all_files=drop_all_files)
    years = get_years_from_filenames("./downloads")
    df=concat_dfs(years=years, commerce=commerce, frequency=frequency)
    df = customs_secrecy_treatment(df) #Should be runned only when exports
    df = insert_country(df)
    df = insert_ncm_description(df)
    return df