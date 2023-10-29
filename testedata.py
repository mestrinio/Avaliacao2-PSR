#!/usr/bin/env python3


# Imports -------------------------------------------------

import datetime

def data():
    # Obtém a data e hora atual
    data_hora_atual = datetime.datetime.now()

    # Acessando os atributos da instância
    dia_da_semana = data_hora_atual.weekday()
    mes = str(data_hora_atual.month)
    dia = str(data_hora_atual.day)
    hora = str(data_hora_atual.hour)
    ano = str(data_hora_atual.year)
    
    if dia_da_semana == 0:
        weekday = 'Mon'
    elif dia_da_semana == 1:
        weekday = 'Tue'
    elif dia_da_semana == 2:
        weekday = 'Wed'
    elif dia_da_semana == 3:
        weekday = 'Thu'
    elif dia_da_semana == 4:
        weekday = 'Fri'
    elif dia_da_semana == 5:
        weekday = 'Sat'
    elif dia_da_semana == 6:
        weekday = 'Sun'
    
    return
    
    
def main():



          
if __name__ == "__main__":
    main()