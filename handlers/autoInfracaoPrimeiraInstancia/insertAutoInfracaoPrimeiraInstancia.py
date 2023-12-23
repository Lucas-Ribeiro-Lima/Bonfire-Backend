from Classes import *
import pandas as pd
import database.mySQL as mySQL
from sqlalchemy import text
 

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

    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()

    try:
        count = dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False)
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            result = f"INFO: {count} autos processados. {csv}"
            print(result, file=t)
        return result
    
    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema realizar o Insert: {csv}"
            print(err, file=t)
            return err, e

def insertIgnoreAutoInfracaoPrimeiraInstanciaCSV(csv):
    
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

    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()

    for index, row in dataFrame.iterrows():
        values_str = ', '.join([f"'{str(value)}'" for value in row.values])
        sql_query = f"INSERT IGNORE INTO auto_infracao (NUM_NOTF, TIP_PENL, NUM_AI, NOM_CONC, COD_LINH, NOM_LINH, NUM_VEIC, IDN_PLAC_VEIC, DAT_OCOR_INFR, DES_LOCA, COD_IRRG_FISC, ARTIGO, DES_OBSE, NUM_MATR_FISC, QTE_PONT, DAT_EMIS_NOTF, DAT_LIMT_RECU, VAL_INFR, DAT_CANC) VALUES ({values_str})"

        try:
            with engine.connect() as connection:
               result = connection.execute(text(sql_query))

            return result.rowcount, None
        
        except Exception as e:
            with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
                err = f"ERRO: problema ao realizar o Insert: {csv}"
                print(err, file=t)
                return err, e

    engine.dispose()