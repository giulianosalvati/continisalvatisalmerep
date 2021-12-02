#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:20:53 2021

@author: giuliano

Obiettivo:
    - Quali sono le fascie orarie con più passeggeri
    - Quali sono le fascie orarie con meno passeggeri
    ripetere tale analisi per ogni borough
    fasce orarie considerate: ogni due ore (?) / ogni ora (?)
    tipo di grafico:  
"""

import numpy  as np
import pandas as pd 
from datetime import datetime
import sys

""" 
Sottoprogramma che legge il file CSV
"""
def fatal_error(message):
    """
    manage a fatal error: print a message and exit program
    :param message: message to be printed
    :return: None
    """
    print(message)
    exit()


def read_csv_file(file_name):
    """
    read a json file and returns data
    manage exceptions
    :param file_name: file to be read
    :return: data structure corresponding to file content
    """
    try:
        fin = open(file_name)
        database_taxi = pd.read_csv(fin)
        fin.close()
        return database_taxi
    except OSError as message:
        fatal_error(message)
""" 
Sottoprogramma che salva il file 
"""

def reduced_database_passeger_count(database_taxi):
    """ 
    Elimino tutte le colonne del dataframe che non mi interessano. 
    Tengo in considerazione solo le colonne:
        tpep_pickup_datetime 
        passenger_count 
        PULocationID 
    
    """
    del database_taxi['VendorID']
    del database_taxi['DOLocationID']
    del database_taxi['trip_distance']
    del database_taxi['tpep_dropoff_datetime']
    del database_taxi['RatecodeID']
    del database_taxi['store_and_fwd_flag']
    del database_taxi['payment_type']
    del database_taxi['fare_amount']
    del database_taxi['extra']
    del database_taxi['mta_tax']
    del database_taxi['tip_amount']
    del database_taxi['tolls_amount']
    del database_taxi['improvement_surcharge']
    del database_taxi['total_amount']
    del database_taxi['congestion_surcharge']
    return database_taxi


def check_month_database(database_taxi,periodo):
    """
    sottoprogramma che in base all'anno e al mese che vengono inseriti in input
    (quelli del file) elimina eventuali dati che non sono di tale periodo.
    ATTENZIONE! tengo conto della data in cui il passeggero è salito nel taxi
    """
    # d = datetime.strptime(database_taxi['tpep_pickup_datetime'],'%Y-%m-%d %H:%M:%S')
    # database_taxi['tpep_pickup_datetime'] = d
    # temp_database = pd.DataFrame(columns=(database_taxi.columns))
    # for data in database_taxi:
    #     if data['tpep_pickup_datetime'].year != periodo.year || data['tpep_pickup_datetime'].month != periodo.month:
    #         temp_database = temp_database
    #         else:
    #             temp_database =  temp_database.append(data)  
    # database_taxi = temp_database                              
    return database_taxi
   

def zero_passenger(database_taxi):
    """
    sottoprogramma che elimina eventuali dati con 0 passeggeri
    """
    database_taxi = database_taxi[database_taxi['passenger_count'] > 0]
    return database_taxi
            

def separate_borough(database_taxi,df_zone,borough_name):
    """
    Sottoprogramma che dati in ingresso il dataframe dei taxi, il dataframe dei codici dei 
    borough e il nome del borough,
    restituisce un dataframe che contiene tutti i dati del dataframe dei taxi che
    hanno come 'PULocationID' un codice che appartiene al borough in ingresso
    """
   
    # borough : DataFrame vuoto che sarà riempito degli eventuali dati che 
    # hanno come 'PULocationID' un codice che corrisponde al borough richiesto
   
    borough = pd.DataFrame(columns=(database_taxi.columns))
    
    # loc_borough : Lista vuota che sarà riempita di tutti i codici che 
    # corrispondono al borough considerato
    
    loc_borough = []
    
    # scorro le righe del dataframe delle zone in modo da riempire la lista 
    # loc_borough definita precedentemente
    
    for i,zona in df_zone.iterrows():
        # se il codice di una zona corrisponde al borough considerato
        if zona[1] == borough_name:
            # aggiungo il codice a loc_borough
            loc_borough = loc_borough + [zona[0]]
            
    # scorro le righe del dataframe dei dati in modo da riempire il dataframe 
    # borough 
   
    for i,data in database_taxi.iterrows():
        # se il dato ha come 'PULocationID' un codice in loc_borough
        if data['PULocationID'] in loc_borough:
            # aggiungo il dato a borough
           borough = borough.append(data)
    
    return borough             
"""
Un sottoprogramma che ci da in uscita un nuovo dataframe che contiene fasce orarie
(da 0 a 23 ogni ora) e numero totale di passeggeri
"""
"""
Grafico dei dati
"""

#### CODICE ####
file_name = input('inserisci un file .csv: ')
database_taxi = read_csv_file(file_name).head(80)
#df_zone è un dataframe che contine i codici identificativi dei 5 borough
df_zone = pd.read_csv('taxi+_zone_lookup.csv')
df_zone['Borough'] = df_zone['Borough'].astype("string")
# in input deve essere specificato l'anno del file
periodo = input('inserisci anno e mese del file (e.s. 2015-02):')
periodo = datetime.strptime(periodo,'%Y-%m')
database_taxi = reduced_database_passeger_count(database_taxi)
database_taxi = check_month_database(database_taxi, periodo)
database_taxi = zero_passenger(database_taxi)

borough_Manhattan = separate_borough(database_taxi, df_zone,'Manhattan')
borough_Queens = separate_borough(database_taxi, df_zone,'Queens')
borough_Bronx = separate_borough(database_taxi, df_zone,'Bronx')
borough_Staten_Island = separate_borough(database_taxi, df_zone,'Staten Island')
borough_Brooklyn = separate_borough(database_taxi, df_zone,'Brooklyn')

print('Fine')