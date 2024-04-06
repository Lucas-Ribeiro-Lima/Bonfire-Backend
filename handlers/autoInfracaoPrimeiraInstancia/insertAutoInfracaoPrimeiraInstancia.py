from Classes import *
import pandas as pd
import Database.databases as databases
from sqlalchemy import text
import numpy as np
 

def insertAutoInfracaoPrimeiraInstanciaCSV(csv):
    try:
        dataFrame = pd.read_csv(csv, header = 0, delimiter='|')

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao processar o arquivo no Load: {csv}"
            print(err, file=t)
        return err, e

    try:
        dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
        dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
            dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%d/%m/%Y")

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao corrigir datas: {csv}"
            print(err, file=t)
            return err, e


    dataFrame = dataFrame.drop(columns=['HORA'])

    engine = databases.mySQL()
    engine = engine.createDatabaseStringConnection()

    try:
        count = dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False)
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            result = f"INFO: {count} autos processados. {csv}"
            print(result, file=t)
        return result, None
    
    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema realizar o Insert: {csv}"
            print(err, file=t)
            return err, e

def insertIgnoreAutoInfracaoPrimeiraInstanciaXLS(xls):
    
    try:
        dataFrame = pd.read_excel(xls, header = 0)

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao processar o arquivo no Load: {xls}"
            print(err, file=t)
        return err, e

    try:
        dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
        dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%Y-%m-%d %H:%M:%S")
        dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%Y-%m-%d")
        dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%Y-%m-%d")
        if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
            dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%Y-%m-%d")

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao corrigir datas: {xls}"
            print(err, file=t)
            return err, e


    dataFrame = dataFrame.drop(columns=['HORA'])
    dataFrame.replace([np.nan], [None], inplace=True)

    engine = databases.mySQL()
    engine = engine.createDatabaseStringConnection()
    counter = 0

    for index, row in dataFrame.iterrows():
        values_dict = row.to_dict()
        sql_query = "INSERT IGNORE INTO auto_infracao (NUM_NOTF, TIP_PENL, NUM_AI, NOM_CONC, COD_LINH, NOM_LINH, NUM_VEIC, IDN_PLAC_VEIC, DAT_OCOR_INFR, DES_LOCA, COD_IRRG_FISC, ARTIGO, DES_OBSE, NUM_MATR_FISC, QTE_PONT, DAT_EMIS_NOTF, DAT_LIMT_RECU, VAL_INFR, DAT_CANC) VALUES (:NUM_NOTF, :TIP_PENL, :NUM_AI, :NOM_CONC, :COD_LINH, :NOM_LINH, :NUM_VEIC, :IDN_PLAC_VEIC, :DAT_OCOR_INFR, :DES_LOCA, :COD_IRRG_FISC, :ARTIGO, :DES_OBSE, :NUM_MATR_FISC, :QTE_PONT, :DAT_EMIS_NOTF, :DAT_LIMT_RECU, :VAL_INFR, :DAT_CANC)"
        try:
            with engine.connect() as connection:
                result = connection.execute(text(sql_query), values_dict)
                if result.rowcount > 0:
                    counter = counter + 1
                connection.commit()

        except Exception as e:
            with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
                err = f"ERRO: problema ao realizar o Insert: {xls}"
                print(err, file=t)
                return err, e       
    engine.dispose()     
    print(counter)
    return counter, None

def insertAutoInfracaoPrimeiraInstanciaXLS(xls):
    try:
        dataFrame = pd.read_excel(xls, header = 0)

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao processar o arquivo no Load: {xls}"
            print(err, file=t)
        return err, e

    try:
        dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
        dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
            dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%d/%m/%Y")

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao corrigir datas: {xls}"
            print(err, file=t)
            return err, e


    dataFrame = dataFrame.drop(columns=['HORA'])

    engine = databases.mySQL()
    engine = engine.createDatabaseStringConnection()

    try:

        count = dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False)
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            result = f"INFO: {count} autos processados. {xls}"
            print(result, file=t)
        return result, None
    
    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema realizar o Insert: {xls}"
            print(err, file=t)
            return err, e