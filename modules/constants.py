DF_COLUMNS = ['year', 'month', 'ncmCode', 'countryCode', 'netWeight', 'fob', 'freight',
       'insurance', 'cif']

MONTH_DICT = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

TITLES_DICT = {
    "imports":{
        "fob":{
            "title_commerce": "FOB importado",
            "title_unit_meassure": "millones de US$",
            "y_unit_meassure": 1_000_000
        },
        "netWeight":{
            "title_commerce": "Peso neto importado",
            "title_unit_meassure": "toneladas",
            "y_unit_meassure": 1_000
        },
        "cif":{
            "title_commerce": "CIF importado",
            "title_unit_meassure": "millones de US$",
            "y_unit_meassure": 1_000_000
        },
        "freight":{
            "title_commerce": "Gastos en fletes para importaciones",
            "title_unit_meassure": "millones de US$",
            "y_unit_meassure": 1_000_000
        },
    },
    "exports":{
        "fob":{
            "title_commerce": "FOB exportado",
            "title_unit_meassure": "millones de US$",
            "y_unit_meassure": 1_000_000
        },
        "netWeight":{
            "title_commerce": "Peso neto exportado",
            "title_unit_meassure": "toneladas",
            "y_unit_meassure": 1_000
        },
    }
}