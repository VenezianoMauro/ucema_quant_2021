import requests
import pandas as pd
import tqdm, sys, os
import numpy as np
#import sqlDB
import datetime as dt
import pickle

from sqlalchemy import create_engine


def scrapear_finviz(pags=range(1,3)):
    """
    :returns
    DataFrame con lista de acciones opcionables
    ticker, company, sector, industry, country, market cap, price, ipo date

    vista_full: aca colocar los numeros segun los filtros de finviz, al filtrar mirar el link para saber cuales son
    los numeros que quieran scrappear

    """

    agents = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    agents += 'Chrome/50.0.2661.75 Safari/537.36'
    header = {"User-Agent": agents, "X-Requested-With": "XMLHttpRequest"}
    vista_simple = '111'
    vista_full = '152&f=sh_opt_option&c=0,1,2,3,4,5,6,65,70'

    df = pd.DataFrame()
    paginas = 1000
    with tqdm.tqdm(total=len(pags), file=sys.stdout) as pbar:
        for pagina in pags:
            pbar.update()
            #https: // finviz.com / screener.ashx?v = 152 & f = sh_opt_option & c = 1, 2, 3, 4, 5, 6, 65, 70
            r = str((pagina)*20 +1)
            url = f'https://finviz.com/screener.ashx?v={vista_full}&r={r}'
            r = requests.get(url, headers = header)
            tablas = pd.read_html(r.text)

            for tabla in tablas:
                valor = tabla[0].values[0]
                if valor == 'No.':
                    data = tabla

                try:
                    if valor.find("Total: ") == 0:
                        paginas = int(valor[7:valor.find('#') - 1]) // 20 + 1
                except:
                    pass
            if pagina == paginas:
                break

            data.columns = data.loc[0]
            data = data.drop(0).drop('No.', axis=1).set_index('Ticker')
            df = pd.concat([df, data])

    return df


def arreglar_datos_finviz(df):

    # Eliminar simbolos no numericos
    df.replace("-",np.nan, inplace = True)
    df.replace({'%': ''}, regex=True, inplace=True)

    return df


def a_numerico(df,columnas):

    for columna in columnas:
        count_T, count_B, count_M, count_K = 0, 0, 0, 0

        for idx, row in df.iterrows():
            try:
                trillones = (row[columna]).find('T')
                billones = (row[columna]).find('B')
                millones = (row[columna]).find('M')
                miles = (row[columna]).find('K')

                if trillones > 0:
                    count_T += 1
                    row[columna] = float(row[columna][:trillones]) * 10 ** 12
                if billones > 0:
                    count_B += 1
                    row[columna] = float(row[columna][:billones]) * 10 ** 9
                if millones > 0:
                    count_M += 1
                    row[columna] = float(row[columna][:millones]) * 10 ** 6
                if miles > 0:
                    count_K += 1
                    row[columna] = float(row[columna][:miles]) * 10 ** 3
            except:
                pass
    return df


def a_flotante(df,columnas):

    for columna in columnas:

        try:
            df[columna] = df[columna].astype(float)
        except:
            try:
                df[columna] = pd.to_numeric((df[columna]))
            except:
                pass

    return df


def nombre_columnas(df):
    columnas_nombres = [c.replace(' ', '_') for c in list(df.columns)]
    df.columns = columnas_nombres

    columnas_nombres = [c.replace('/', '_') for c in list(df.columns)]
    df.columns = columnas_nombres

    return df


def a_datetime(df):
    df["IPO_Date"] = pd.to_datetime(df["IPO_Date"])

    return df


def poner_minusculas(df):
    df = df.reset_index()
    df.columns = ["ticker","company","sector","industry","country","market_cap","price","ipo_date"]
    df = df.set_index("ticker")

    return df


def back_up_pickle_df(data, name):

    data.to_pickle(name)

    return True


def up_pickle_df(name):

    pickle_in = open(name, 'rb')

    return pickle.load(pickle_in)


def crearTablaFinviz(name_file="finviz",pags=range(1)):

    """ Descarga todas las acciones que son shorteables con alguna informacion adicional y lo sube a la DB """

    finviz = scrapear_finviz(pags=pags)
    finviz = arreglar_datos_finviz(finviz)
    finviz = a_numerico(finviz, ["Market Cap"])
    finviz = a_flotante(finviz, ["Price"])
    finviz = nombre_columnas(finviz)
    finviz = a_datetime(finviz)
    finviz = poner_minusculas(finviz)

    ### SOLO PARA GUARDAR EN SQL ###
    # .tabla_finviz(nombre=nombre)
    #
    # # Back up DB
    # sqlDB.backup(finviz,nombre=nombre,if_exists="append")

    back_up_pickle_df(finviz, name_file)

    return finviz


if __name__ == '__main__':

    """   / / / TABLA FINVIZ DE STOCKS OPCIONABLES / / /   """

    name = 'finviz_scrapping'
    data = crearTablaFinviz(name_file=name, pags=range(250))
    print(data.info())

    print(up_pickle_df(name))


