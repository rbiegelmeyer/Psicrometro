import math


# Pressao de Saturacao do Vapor da agua
def pSatVapor(temperatura): 
    temperatura += 273.15 # Converte Temperatura de °C para Kelvin

    C1 = -5674.5359
    C2 = 6.3925247
    C3 = -0.009677843
    C4 = 0.00000062215701
    C5 = 2.0747825E-09
    C6 = -9.484024E-13
    C7 = 4.1635019
    C8 = -5800.2206
    C9 = 1.3914993
    C10 = -0.048640239
    C11 = 0.000041764768
    C12 = -0.000000014452093
    C13 = 6.5459673

    if (temperatura <= 273.15):
        return math.exp(C1/temperatura + C2 + C3*temperatura + C4*temperatura**2 + C5*temperatura**3 + 
                          C6*temperatura**4 + C7*math.log(temperatura)) / 1000
    else:
        return math.exp(C8/temperatura + C9 + C10*temperatura + C11*temperatura**2 + C12*temperatura**3 + 
                          C13*math.log(temperatura)) / 1000

# Conteudo de Umidade na Saturacao
def conteudoDeUmidadeSat(temperatura,pressao):
    pws = pSatVapor(temperatura)
    return 0.62198*(pws/(pressao-pws))


# Conteudo de Umidade
def conteudoDeUmidade(tbs,tbu,pressao):
    ws_bu = conteudoDeUmidadeSat(tbu,pressao)

    if (tbs >= 0):                         
        return (((2501 - 2.326*tbu)*ws_bu - 1.006*(tbs - tbu))/
                  (2501 + 1.86*tbs - 4.186*tbu))
    else:                                 
        return (((2830 - 0.24*tbu)*ws_bu - 1.006*(tbs - tbu))/
                  (2830 + 1.86*tbs - 2.1*tbu))


# Grau de Saturacao
def grauSaturacao(_W,_ws_bs):
    return _W/_ws_bs


# Umidade Relativa
def ur(tbs,tbu,pressao):
    W = conteudoDeUmidade(tbs,tbu,pressao)
    _ws_bs = conteudoDeUmidadeSat(tbs,pressao)

    u = grauSaturacao(W,_ws_bs)

    pws_bs = pSatVapor(tbs)

    return u/(1-(1-u)*(pws_bs/pressao))*100






# Ponto de Orvalho
def Dew_point(tbs,tbu,P):

    ''' Function to compute the dew point temperature (deg C)
        From page 6.9 equation 39 and 40 in ASHRAE Fundamentals handbook (2005)
            P = ambient pressure [kPa]
            W = humidity ratio [kg/kg dry air]
        Valid for Dew Points less than 93 C
    '''
    W = conteudoDeUmidade(tbs,tbu,P)

    C14 = 6.54
    C15 = 14.526
    C16 = 0.7389
    C17 = 0.09486
    C18 = 0.4569
    
    Pw = P * W / (0.62198 + W)
    alpha = math.log(Pw)
    Tdp1 = C14 + C15*alpha + C16*alpha**2 + C17*alpha**3 + C18*Pw**0.1984
    Tdp2 = 6.09 + 12.608*alpha + 0.4959*alpha**2
    if Tdp1 >= 0:
        result = Tdp1
    else:
        result = Tdp2
    return result