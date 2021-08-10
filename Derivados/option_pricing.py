import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

## este es el código de Maurette para cálculo de opción europea 
## usando árbol binomial
## de nuevo: con un solo # son los comentarios de él
## con ## son los míos

## parece largo, pero es puro comentario

## nota : * es multiplicación y ** es potencia. 
## es decir: 2*3 = 6 y 2**3= 8 

def opcion_europea_bin(tipo, S, K, T, r, sigma, div, pasos):

    #auxiliares
    
    ## dt: delta t, es el largo del paso que doy. Time to maturity / pasos.
    ## Lo que estamos haciendo es dividir la vida de la opción  en muchos intervalos
    ## de tiempo de tamaño dt.
    dt = T / pasos
    
    ## tasas: la tasa hacia adelante y la tasa para descontar
    ## son las continuas, e a la r*dt. La unica diferencia es que si
    ## tenes dividendos, se los restas a la risk free
    tasa_forward = math.exp((r - div) * dt)
    descuento = math.exp(-r * dt)

    #modelo CRR
    ## En cada intervalo de tiempo vamos a asumir que el precio del subyacente se puede mover
    ## hacia cualqueira de dos precios: S*u o S*d  (S es el precio)
    ## Entonces vamos a definir esos dos valores que multiplican al precio S: d y u
    ## u es lo que sube el precio de la acción y d lo que baja 
    ## en general u > 1 y d < 1. O sea: si S0 es el precio de la acción al inicio del arbol,
    ## si el precio de la acción sube (la rama de arriba) te va a quedar en s0 * u. 
    ## si el precio de la acción baja (la rama de abajo) te va a quedar en s0 * d
    
    ## Siguiendo las ecuaciones del hull (edicion 10, pagina 451. Ecuaciones 21.3 a 21.7)
    u = math.exp(sigma * math.pow(dt, 0.5))  ## ecuacion 21.5
    d = 1 / u ## ecuacion 21.3
    
    #probabilidad de riesgo neutral 
    ## cual es la probabilidad en un mundo risk-neutral de que la acción suba
    ## en el hull (edicion 10, pagina 285) muestra que esta tambien es la proba en el mundo real
    ## ademas de la proba en el mundo risk-neutral
    q_prob = (tasa_forward - d) / (u - d) ## ecuacion 21.4

    #Precios finales
    ## instancia una vector de 0 del tamaño de los pasos + 1
    ## aca va a guardar los precios finales de la acción
    ST_precios=np.zeros((pasos+1))
    
    ## y acá genera los precios finales de la acción
    ## lo que está haciendo es generar potencias de u
    ## ponele que hay 4 pasos: 
    ## 2 * i - pasos te va a generar los siguientes valores:
    ## 2*0 - 4 = -4
    ## 2*1 -4 = -2
    ## 2*2 - 4 = 0
    ## 2*3 - 4 = 2 
    ## 2*4 - 4 = 4
    ## si miras la pagina 452 del hull (edicion 10), figura 21.2 
    ## son los valores del ultimo timestep
    ## el detalle a tener en cuenta es que d = 1/u
    ## entonces ese u ** -2 es como tener d ** 2
    for i in range(0,pasos+1):
        ST_precios[pasos-i] = math.pow(u, 2 * i - pasos) * S
        
    
    ## aca va a generar una matriz de 0 para guardar los precios
    ## de las opciones
    #Matriz de precios de la opcion
    opcion_precios = np.zeros((pasos+1, pasos+1))
    
    ## calculamos el valor de las opciones sobre los precios finales
    #Payoff
    for i in range (0, pasos+1):
        if tipo == "P":
            ## si es un put, para el precio final de las opciones calculamos
            ## el maximo entre 0 y la diferencia entre K (el strike) y el 
            ## precio de la acción que calculamos antes
            opcion_precios[i][pasos] = max(0, (K - ST_precios[i]))
        elif tipo == "C":
            ## si es un call, para el precio final de las opciones calculamos
            ## el maximo entre 0 y la diferencia entre el precio de la acción que calculamos antes
            ## y K (el strike)
            opcion_precios[i][pasos] = max(0, (ST_precios[i] - K))
    
    ## ahora ya tenemos el precio final de las acciones y de las opciones
    ## lo que hacemos es ir para atrás por el arbol y lo vamos completando.
    ## en este caso, Maurette lo representa con una matriz (que va a quedar esparsa)
    
    for j in range(1, pasos+1):
        for i in range(0, pasos+1 - j):
            ## arranca de arriba a la derecha de la matriz y se va moviendo
            ## hacia abajo (i) y hacia izquierda (j)
            
            ## aca hay una formula medio larga:
            ## hace el descuento una suma:
            ## (q_prob * opcion_precios[i][pasos - j + 1] + (1  - q_prob) * opcion_precios[i + 1][pasos - j + 1])
            ## el primer termino de la suma es q_prob (que dijimos que es la proba risk-neutral de que la accion suba)
            ## multiplicado por opcion_precios[i][pasos - j + 1], o sea que lo que hace es tomar la misma fila
            ## y mirar el numero de la derecha. O sea, lo que está viendo es el precio de la opción si el subyacente sube
            ## y del otro lado tenemos 1 - qprob (o sea, la probabilidad risk-neutrla de que le subyacente baje)
            ## multiplicado por el precio de la opcion si el subyacente baja (o sea, el numero que esta a la derecha
            ## y en la fila de abajo de la matriz de precios de opciones)
            ## o sea, que lo que tenes ahi es:
            ## precio de la opcion si sube el subyacente * probabilidad de que suba + precio de la opcion si el subyacente
            ## baja * probabilidad de que baje (la esperanza)
            ## y eso lo multiplica por la tasa de descuento
            
            ## con eso se va moviendo para atrás en la matriz de precios de opciones y va completando la matriz de 0
            ## arranca con los precios de adelante, calcula la esperanza y descuenta, luego se mueve para atras y repite
            
            opcion_precios[i][pasos - j] = descuento * (q_prob * opcion_precios[i][pasos - j + 1] + (1  - q_prob) * opcion_precios[i + 1][pasos - j + 1])

    ## la opcion del principio de todo es el precio que deberia tener la opcion
    precio_BIN = opcion_precios[0][0]
    return precio_BIN


## tenemos la otra funcion: el calculo de precio para opciones americanas
def opcion_americana_bin(tipo, S, K, T, r, sigma, div, pasos):

    ## la priemra parte es IGUAL (se podria escribir una sola funcion que abarque ambos tipos)
    dt = T / pasos
    tasa_forward = math.exp((r - div) * dt)
    descuento = math.exp(-r * dt)
    u = math.exp(sigma * math.pow(dt, 0.5))
    d = 1 / u
    q_prob = (tasa_forward - d) / (u - d)

    #Precios finales
    ST_precios=np.zeros((pasos+1))

    for i in range(0,pasos+1):
        ST_precios[pasos-i] = math.pow(u, 2 * i - pasos) * S

    #Matriz de Opcion
    opcion_precios = np.zeros((pasos+1, pasos+1))

    #Payoff
    for i in range (0, pasos+1):
        if tipo == "P":
            opcion_precios[i][pasos] = max(0, (K - ST_precios[i]))
        elif tipo == "C":
            opcion_precios[i][pasos] = max(0, (ST_precios[i] - K))
    
    
    ## hasta aca todo igual, acá es donde arranca la diferencia
    for j in range(1, pasos+1):
        for i in range(0, pasos+1 - j):
            
            ## calcula el precio como si fuera una europea (igual que en la funcion anterior)
            eur = q_prob * opcion_precios[i][pasos - j + 1] + (1  - q_prob) * opcion_precios[i + 1][pasos - j + 1]
            if tipo == "P":
                ## si es un put, se queda con el máximo entre el precio de la europea correspondiente
                ## y K (el strike) - el S que tendrías en ese tiempo. O sea, te quedas con el mejor
                ## entre el precio y lo que te queda si la ejercés
                ## eso lo descontas
                opcion_precios[i][pasos - j] = descuento * max(eur, K - S * math.pow(u,-2*i+pasos-j))
            elif tipo == "C":
                ## lo mismo para el call: es el maximo entre la europea y el ejercicio, descontado
                opcion_precios[i][pasos - j] = descuento * max(eur, S * math.pow(u,-2*i+pasos-j) - K)
    
    ## hay que tener en cuenta que, aunque estamos tomando un parámetro para dividendos al principio del código
    ## despues no se corrije por dividendos en el cálculo del árbol. 
    ## igual maurette aclaró que para hacer codigo productivo en vez de usar esto, es recomendable usar
    ## quantlib
    
    return opcion_precios[0][0]



## acá va a implementar de otra manera, más rápida, el arbol binomial
## esta es la formula cerrada que vemos en clase 3 diapo 32

import operator as op
from functools import reduce

## aca define una funcion para calcular las combinaciones de n tomadas de a r
## por ejemplo ncr(4,2) sería las combinaciones de 4 tomadas de a 2 
## o sea 6
## esta funcion es una forma rápida de calcularlo nada mas:
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1) 
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom 


def opcion_europea_bin_c(tipo, S, K, T, r, sigma, div, pasos):
    
    ## al principio es igual
    
    #auxiliares
    dt = T / pasos
    tasa_forward = math.exp((r - div) * dt)
    descuento = math.exp(-r * dt)

    #modelo CRR
    u = math.exp(sigma * math.pow(dt, 0.5))
    d = 1 / u
    #probabilidad de riesgo neutral
    q_prob = (tasa_forward - d) / (u - d)

    ## aca es donde empieza a ser diferente
    ## define una variable temp
    ## esto es un acumulador donde va a ir sumandole cosas
    ## sirve para hacer una sumatoria
    temp = 0
    
    ## itera sobre los pasos (en vez de del r de la funcion auxiliar ncr se va a llamar k)
    for k in range(pasos):
        if tipo == "C":
            ## aca calcula el payoff para el último tiempo. 
            ## supongamos que tenes 4 pasos:
            ## Cuando k = 0, te queda max(0, S * 1 * d**4 - K)
            ## Cuando k = 1, te queda max(0, S * u * d**3 - K)
            ## Cuando k = 2, te queda max(0, S * (u**2) * (d**2) - K)
            ## Cuando k = 3, te queda max(0, S * (u**3) * (d) - K)
            
            ## me parece que falta un paso más, pero k itera en range(pasos)
            ## o sea que si pasos = 4, range(pasos) vale 0,1,2,3
            ## por ahi habría que corregirlo a range(pasos+1)
            
            ## o sea, te vas moviendo desde el caso en el que el precio de la acción bajó
            ## en todos los pasos. Despues al que bajó en todos los pasos menos 1 y subio en 1. 
            ## DEspues al que bajó en todos los pasos menos 2 de ellos y subio en dos pasos
            ## y así hasta el caso en que el precio de la acción subió en todos los pasos
            
            payoff = max(0, S * math.pow(u,k) * math.pow(d,pasos-k)-K)
        elif tipo == "P":
            
            ## lo mismo para el put, pero con su payoff
            payoff = max(0, K - S * math.pow(u, k) * math.pow(d, pasos - k))
        
        ## y le suma a temp 
        ## aca a temp le va sumando el valor del combinatorio
        ## multiplicado por la probabilidad de llegar al nodo en el que está
        ## por el payoff correspondiente
        ## (ver segunda ecuacion de la diapo 32 de la clase 3 del modulo de Maurette)
        temp = temp +ncr(pasos, k) * math.pow(q_prob,k) * math.pow((1-q_prob),pasos-k) * payoff
    
    ## y lo que le queda, lo descuenta
    precio_BIN_c = math.exp(-r*T)*temp
    return precio_BIN_c


## esto no tiene mucho misterio: es la formula de black and scholes
## es una cuenta nomás
## lo unico por ahi a tener en cuenta es norm.cdf es la normal acumulada

def opcion_europea_bs(tipo, S, K, T, r, sigma, div):
    #Defino los ds
    d1 = (math.log(S / K) + (r - div + 0.5 * sigma * sigma) * T) / sigma / math.sqrt(T)
    d2 = (math.log(S / K) + (r - div - 0.5 * sigma * sigma) * T) / sigma / math.sqrt(T)

    if (tipo == "C"):
        precio_BS = math.exp(-div*T) *S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        
    elif (tipo == "P"):
        precio_BS = K * math.exp(-r * T) * norm.cdf(-d2) - math.exp(-div*T) * S * norm.cdf(-d1)
        
    return precio_BS