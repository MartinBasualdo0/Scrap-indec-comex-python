def customs_secrecy_treatment(df):
    df['netWeight']=df['netWeight'].astype(str).apply(lambda x: x.replace(',','.'))
    df['fob']=df['fob'].astype(str).apply(lambda x: x.replace(',','.'))
    df.loc[df['netWeight'].str.contains("s"), 'netWeight'] = "0"
    df.loc[df['fob'].str.contains("s"), 'fob'] = "0"
    df['netWeight']=df['netWeight'].astype(float)
    df['fob']=df['fob'].astype(float)
    return df