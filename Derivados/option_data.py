import yfinance as yf
import pandas as pd
import numpy as np
import datetime

## voy a definir una funcion que baje los calls y puts de un ticker
def generar_df_opciones(ticker):

    ## instancio el ticker
    data = yf.Ticker(ticker)

    ## me traigo los vencimientos
    vencimientos = data.options

    ## los calls para ese vencimiento
    calls = [data.option_chain(x)[0] for x in vencimientos]
    calls = pd.concat(calls)

    ## los puts para ese vencimiento
    puts = [data.option_chain(x)[1] for x in vencimientos]
    puts = pd.concat(puts)

    ## uno ambos
    opciones = pd.concat([calls,puts]).reset_index(drop = True)
    ## le agrego el spot
    opciones.loc[:,"spot"] = data.history().Close.values[-1]
    
        
    ## le agrego el ticker
    opciones.loc[:,"ticker"] = ticker
    
    return opciones


## defino una funcion que, a partir del dataframe de base, me devuelva un df completo
## con toda la data que pide maurette
def get_full_data(df):
    callput = df.iloc[:,0].str[10]
    df.loc[:,"CallPut"] = callput

    ## tomo 4to y 5to del ticker de la opcion
    ## la convierto en int y le sumo 2020, con eso obtengo el año
    year = 2000 + df.iloc[:,0].str[4:6].astype(int)

    ## tomo la posicion 6 y 7 del ticker para el mes
    month = df.iloc[:,0].str[6:8].astype(int)

    ## tomo la posicion 8 y 9 del ticker para el dia
    day = df.iloc[:,0].str[8:10].astype(int)

    ## voy a tomar la fecha de hoy y se la voy a restar la fecha de vencimiento, 
    ## con eso obtengo el time to maturity
    hoy = datetime.date.today()

    ## zip lo que hace es unir año, mes y dia. Cuando itera me devuelve le primer año de la lista
    ## con el primer mes de la lista con el primer día de la lista. 
    ## Despues el segundo año de la lista, con el segundo mes, con el segundo día y así.
    ## para cada uno de estos genero una fecha
    expiry_datetime = [datetime.date(y, m, d) for y,m,d in zip(year, month, day)]

    ## y para cada fecha, le resto la fecha de hoy
    ttm = [(d - hoy).days for d in expiry_datetime]
    df.loc[:,"ttm"] = ttm

    ## defino moneyness como el ratio entre el spot y el strike
    df.loc[:,"moneyness"] = df.spot/df.strike
    
    ## reordeno las columnas
    df = df.iloc[:,[0,-4,-5,-3,2,-2, 3, 4, 5, 10, -1]]
    df.columns = ["Especie", "Ticker", "Spot", "CallPut","Strike", "TTM", "Last", "Bid", 
                  "Ask", "impliedVolatility","Moneyness"]
    return df
