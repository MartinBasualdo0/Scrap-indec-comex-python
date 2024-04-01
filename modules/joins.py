import pandas as pd

def get_dic_countries():
    df_countries=pd.read_csv('./data/CE_PAIS.csv', sep=';', dtype={'CCOD_ASOC':str})
    df_countries['countryFinalCode']=df_countries.CCOD_ASOC.fillna(df_countries.CCOD_PAIS)
    dic_countries=dict(zip(df_countries.CCOD_PAIS,df_countries.CDESCRI))
    df_countries['countryFinalDescritpion'] = df_countries.countryFinalCode.apply(lambda x: dic_countries[x])
    dic_cod_countries=dict(zip(df_countries.CCOD_PAIS,df_countries.countryFinalCode))
    # asociados=df_countries[~df_countries.CCOD_ASOC.isna()] #para ver cod con asociados
    dic_asociated_countries=dict(zip(df_countries.CCOD_PAIS,df_countries.countryFinalDescritpion))
    # df_countries=df_countries[['countryFinalCode','countryFinalDescritpion']]
    #df_countries
    return dic_countries, dic_cod_countries, dic_asociated_countries

def insert_country(df):
    dic_countries, dic_cod_countries, dic_asociated_countries = get_dic_countries()
    df.insert(4,'countryDescription',df.countryCode.apply(lambda x: dic_countries[x]))
    df.insert(5,'countryFinalCode',df.countryCode.apply(lambda x: dic_cod_countries[x]))
    df.insert(6,'countryFinalDescritpion',df.countryCode.apply(lambda x: dic_asociated_countries[x]))
    df = df.fillna(0)
    df = df.drop('countryCode',axis=1)
    df = df.drop('countryDescription', axis = 1)
    return df

def insert_ncm_description(df):
    df_descriptions = pd.read_csv('./data/CE_ENMIENDA.csv',sep=';',dtype={'ncm':str,'cnro_enmienda':int})
    ncm_descript_dict = dict(zip(df_descriptions.ncm, df_descriptions.ncm_descri))
    df["ncmDescription"] = df.ncmCode.map(ncm_descript_dict)    
    return df
