import pandas as pd
from typing import Literal
from modules.constants import TITLES_DICT
import plotly.graph_objects as go

def shorten_description(descri, length = 45):
    if len(descri)>=length:
        return descri[:length]+'...'
    else:
        return descri
    
def get_monthly_date_df(year_from:str, df:pd.DataFrame, frequency:Literal["Y","M"], ):
    if frequency == "M":
        start_series = f"{df.month.iloc[0]}/01/{year_from}"
        end_series = f"{int(df.month.iloc[-1])+1}/01/{int(df.year.iloc[-1])}"
    else:
        start_series = f"{year_from}"
        end_series = str(int(df.year.iloc[-1])) #!I do not want to see if the year has not finished
        # This could be a problem if the publication is for december
    df_dates = pd.DataFrame({
    'date': pd.date_range(start=start_series, end=end_series, freq=frequency)
    })
    df_dates["year"] = df_dates.date.dt.year.astype(str)
    if frequency == "M":
        df_dates["month"] = df_dates.date.dt.month.astype(str).apply(lambda x: x.zfill(2))
    df_dates = df_dates.drop("date", axis=1)
    return df_dates

def filter_dataframe_for_plot(df:pd.DataFrame, ncm_code:str, year_from:str):
    ncm_code=str(ncm_code)
    temp = df.copy()
    temp = temp[temp['year'] >= str(year_from)].reset_index(drop = True)
    temp=temp[temp.ncmCode == ncm_code].reset_index(drop=True)
    return temp

def prepare_dataframe_for_plot(df:pd.DataFrame, frequency:str, year_from:str,include_countries:bool):
    aggrupation = ["year", "month"] if frequency == "M" else ["year"]
    if include_countries == False:
        df=df.groupby(aggrupation,as_index=False).sum(numeric_only=True)
    df_dates = get_monthly_date_df(year_from=year_from, df = df, frequency=frequency,)
    df = df_dates.merge(df, how="left", on=aggrupation)
    return df


def bar_plot(df:pd.DataFrame,
             commerce:Literal["imports", "exports"],
             year_from:str,
             frequency:Literal["Y","M"], 
             variable:Literal["fob","cif","insurance", "freight", "netWeight"],
             ncm_code:str = '12019000',
             include_countries:bool = True):
    df = filter_dataframe_for_plot(df, ncm_code,year_from)
    descri = shorten_description(df.ncmDescription.iloc[0], length = 60)
    df = prepare_dataframe_for_plot(df, frequency, year_from, include_countries)        
    titles_dict = TITLES_DICT[commerce][variable]
    title_commerce = titles_dict["title_commerce"]
    title_unit_meassure = titles_dict["title_unit_meassure"]
    y = df[variable] / titles_dict["y_unit_meassure"]
    x = df.year if frequency == "Y" else df.month + "/" + df.year

    fig = go.Figure()
    if include_countries:
        df = df.pivot_table(values=variable, index="year", columns="countryFinalDescritpion")
        for country in df.columns:
            fig.add_trace(go.Bar(name = country,x = df.index, y = df[country]/ titles_dict["y_unit_meassure"]))
    else:
        fig.add_trace(go.Bar(x = x, y = y ))
    fig.update_xaxes(type='category',title_text="")
    fig.update_yaxes(title_text=title_unit_meassure.capitalize(), tickformat=',')
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide',
                      title_text = f"{title_commerce} de: <br>\"{descri}\"<br><sup>En {title_unit_meassure}</sup>",
                      barmode='relative',separators=",.", 
                      height=600, width=1000, 
                      template = 'none',
                      legend = dict(yanchor="bottom", xanchor="left", orientation="h", y = .95
                  ))
    note = f'Fuente: @MartinBasualdo0 en base a INDEC'
    # note = f'Fuente: @MartinBasualdo0 en base a INDEC. Datos del {ultimo_anio_disponible} hasta {ultimo_mes_disponible}'
    fig.add_annotation(showarrow=False, text=note,font=dict(size=12), xref='paper', x=0.3, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)
    return fig