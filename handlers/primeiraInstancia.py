import numpy as np
import pandas as pd
from classes import *
from sqlalchemy import text, insert
from repositories import database
from handlers import log
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrReadingFile

def insert_ignore_mysql(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).values(data).prefix_with("IGNORE")
    result = conn.execute(stmt)
    return result.rowcount

def getPrimeiraInstancia(date):
    """Recupera os autos de infração de primeira instancia"""
    engine = database.mySQL().createDatabaseStringConnection()
    try:
        with engine.connect():
            query = f"SELECT * FROM auto_infracao WHERE DAT_EMIS_NOTF >= '{date}'"
            dataFrame = pd.read_sql(query, engine)
            dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'])
            dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'])
            dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'])

            jsonData = dataFrame.to_json(orient='records')

        engine.dispose()
        return jsonData
        
    except Exception as e:
        log.HandleErrorLog(e)
        raise("Erro ao recuperar os autos de primeira instância", 500)
    

def checkAutoInfracaoPrimeiraInstancia(csv):
    """Realiza a verificação dos autos de infração no banco de dados"""
    try:
        dataFrame = pd.read_csv(csv, header = 0, delimiter=';')
        values = dataFrame['NUM_AI'].unique()

    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile("Erro ao ler o arquivo CSV", 500)

    engine = database.mySQL().createDatabaseStringConnection()
    try:
      counter = 0
      rows_counter = 0
      rows_notpresent = []
      for value in values:
          query = f"SELECT * FROM auto_infracao WHERE NUM_AI = '{value}'"

          result_df = pd.read_sql(query, engine)
          rows = result_df.shape[0]
          if rows > 0:
              rows_counter = rows_counter +1
          counter = counter +1
          if rows == 0:
              rows_notpresent.append(value)

      engine.dispose()
      return rows_counter, counter, rows_notpresent

    except Exception as e:
      log.HandleErrorLog(e)
      raise ErrGetData("Erro ao validar os dados no banco de dados", 500)


def insertAutoInfracaoPrimeiraInstanciaCSV(csv):
    """Insere os autos de infração no banco de dados apartir de um arquivo CSV"""
    try:
        dataFrame = pd.read_csv(csv, header = 0, delimiter=';')
        dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
        dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        dataFrame["VAL_INFR"] = dataFrame['VAL_INFR'].map(lambda x: pd.to_numeric(str(x).replace(',', '.')))
        if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
            dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%d/%m/%Y")
        dataFrame = dataFrame.drop(columns=['HORA'])

    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile(f"Erro ao processar o arquivo CSV. {e}", 500)

    engine = database.mySQL().createDatabaseStringConnection()
    try:
        count = dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False, method=insert_ignore_mysql)
        log.HandleSuccessLog(f"INFO: {count} autos processados. FILE: {csv}")
        return count
  
    except Exception as e:
      log.HandleErrorLog(e)
      raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {csv}', 500)


def insertIgnoreAutoInfracaoPrimeiraInstanciaXLS(xls) -> int:
    """Insere os autos de infração no banco de dados apartir de um arquivo XLS ignorando os duplicados"""
    try:
        dataFrame = pd.read_excel(xls, header = 0)            

    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
      dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
      dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%Y-%m-%d %H:%M:%S")
      dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%Y-%m-%d")
      dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%Y-%m-%d")
      if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
          dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%Y-%m-%d")

      dataFrame = dataFrame.drop(columns=['HORA'])
      dataFrame.replace([np.nan], [None], inplace=True)
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    engine = database.mySQL().createDatabaseStringConnection()
    counter = 0
    try:
      for row in dataFrame.iterrows():
          values_dict = row.to_dict()
          sql_query = "INSERT IGNORE INTO auto_infracao (NUM_NOTF, TIP_PENL, NUM_AI, NOM_CONC, COD_LINH, NOM_LINH, NUM_VEIC, IDN_PLAC_VEIC, DAT_OCOR_INFR, DES_LOCA, COD_IRRG_FISC, ARTIGO, DES_OBSE, NUM_MATR_FISC, QTE_PONT, DAT_EMIS_NOTF, DAT_LIMT_RECU, VAL_INFR, DAT_CANC) VALUES (:NUM_NOTF, :TIP_PENL, :NUM_AI, :NOM_CONC, :COD_LINH, :NOM_LINH, :NUM_VEIC, :IDN_PLAC_VEIC, :DAT_OCOR_INFR, :DES_LOCA, :COD_IRRG_FISC, :ARTIGO, :DES_OBSE, :NUM_MATR_FISC, :QTE_PONT, :DAT_EMIS_NOTF, :DAT_LIMT_RECU, :VAL_INFR, :DAT_CANC)"
          with engine.connect() as conn:
              result = conn.execute(text(sql_query), values_dict)
              if result.rowcount > 0:
                  counter = counter + 1
              conn.commit()
          engine.dispose()
          return counter
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrInsertData(f'Erro ao inserir o auto de infração no banco de dados', 500)       


def insertAutoInfracaoPrimeiraInstanciaXLS(xls):
    """Insere os autos de infração no banco de dados apartir de um arquivo XLS"""
    try:
        dataFrame = pd.read_excel(xls, header = 0)            

    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
        dataFrame['DAT_OCOR_INFR'] = dataFrame['DAT_OCOR_INFR'].astype(str) + " " + dataFrame['HORA'].astype(str)
        dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        if 'DAT_CANC' in dataFrame.columns and not dataFrame['DAT_CANC'].isnull().all():
            dataFrame['DAT_CANC'] = pd.to_datetime(dataFrame['DAT_CANC'], format="%d/%m/%Y")

        dataFrame = dataFrame.drop(columns=['HORA'])
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    engine = database.mySQL().createDatabaseStringConnection()
    try:
        count = dataFrame.to_sql('auto_infracao', engine, if_exists='append', index=False)
        log.HandleSuccessLog(f"INFO: {count} autos processados - {xls}")
        return count
    
    except Exception as e:
      log.HandleErrorLog(e)
      raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {xls}', 500)