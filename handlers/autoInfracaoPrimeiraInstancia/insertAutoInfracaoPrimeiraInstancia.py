from Classes import *
import pandas as pd
import database.mySQL as mySQL
 

def insertAutoInfracaoPrimeiraInstanciaCSV(csv):
    dataFrame = pd.read_csv(csv, header = 0, delimiter='|')
    dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
    dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
    dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
    dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%d/%m/%Y")
    dataFrame = dataFrame.drop(columns=['HORA'])

    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()

    dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False)
    count = len(dataFrame.index)

    return count