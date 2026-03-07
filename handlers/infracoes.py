from warnings import deprecated

import numpy as np
import pandas as pd
from sqlalchemy import text, insert
from handlers.log import logger

from repositories.database import MySQL
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrReadingFile

engine = MySQL().get_connection()

def insert_ignore_mysql(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).values(data).prefix_with("IGNORE")
    result = conn.execute(stmt)
    return result.rowcount


def get_infracoes(date, ai):
    """Recupera os autos de infração"""
    try:
        with engine.connect() as conn:
            query = "SELECT * FROM auto_infracao WHERE 1 = 1"
            params = {}

            if ai is not None:
                query += " AND NUM_AI LIKE :ai"
                params["ai"] = f"%{ai}%"

            if date is not None:
                query += " AND DAT_EMIS_NOTF >= :date"
                params["date"] = date

            query += " LIMIT 200"
            result = conn.execute(text(query), params)

            rows = result.mappings().all()
            json_data = [dict(row) for row in rows]

        engine.dispose()
        return json_data

    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData("Erro ao recuperar dados", 500)


def check_infracoes(csv):
    """Realiza a verificação dos autos de infração no banco de dados"""
    try:
        data_frame = pd.read_csv(csv, header=0, delimiter=';')
        values = data_frame['NUM_AI'].unique()

    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile("Erro ao ler o arquivo CSV", 500)

    try:
        counter = 0
        rows_counter = 0
        rows_not_present = []
        for value in values:
            query = f"SELECT * FROM auto_infracao WHERE NUM_AI = '{value}'"

            result_df = pd.read_sql(query, engine)
            rows = result_df.shape[0]
            if rows > 0:
                rows_counter = rows_counter + 1
            counter = counter + 1
            if rows == 0:
                rows_not_present.append(value)

        engine.dispose()
        return rows_counter, counter, rows_not_present

    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData("Erro ao validar os dados no banco de dados", 500)


def insert_infracoes_csv(csv):
    """Insere os autos de infração no banco de dados a partir de um arquivo CSV"""
    try:
        data_frame = pd.read_csv(csv, header=0, encoding="latin_1", delimiter=';')
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        data_frame["VAL_INFR"] = data_frame['VAL_INFR'].map(lambda x: pd.to_numeric(str(x).replace(',', '.')))
        if 'DAT_CANC' in data_frame.columns and not data_frame['DAT_CANC'].isnull().all():
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%d/%m/%Y")
        data_frame = data_frame.drop(columns=['HORA'])

    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f"Erro ao processar o arquivo CSV. {e}", 500)

    try:
        count = data_frame.to_sql('auto_infracao', engine, if_exists='append', index=False, method=insert_ignore_mysql)
        logger.systemLog(f"INFO: {count} autos processados. FILE: {csv}")
        return count

    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {csv}', 500)


def insert_infracoes_xls(xls, ignore):
    """Insere os autos de infração no banco de dados a partir de um arquivo XLS"""
    try:
        data_frame = pd.read_excel(xls, header=0)

    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%Y-%m-%d %H:%M:%S")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%Y-%m-%d")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%Y-%m-%d")
        if 'DAT_CANC' in data_frame.columns and not data_frame['DAT_CANC'].isnull().all():
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%Y-%m-%d")

        data_frame = data_frame.drop(columns=['HORA'])
        data_frame.replace([np.nan], [None], inplace=True)
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    counter = 0
    try:
        for row in data_frame.iterrows():
            values_dict = row.to_dict()
            sql_query = (f'''
            INSERT {"IGNORE" if ignore else ""} INTO auto_infracao 
                         (NUM_NOTF, TIP_PENL, NUM_AI, NOM_CONC, COD_LINH, NOM_LINH, NUM_VEIC, IDN_PLAC_VEIC, 
                         DAT_OCOR_INFR, DES_LOCA, COD_IRRG_FISC, ARTIGO, DES_OBSE, NUM_MATR_FISC, QTE_PONT, 
                         DAT_EMIS_NOTF, DAT_LIMT_RECU, VAL_INFR, DAT_CANC) 
                         VALUES (:NUM_NOTF, :TIP_PENL, :NUM_AI, :NOM_CONC, :COD_LINH, :NOM_LINH, :NUM_VEIC, :IDN_PLAC_VEIC, 
                         :DAT_OCOR_INFR, :DES_LOCA, :COD_IRRG_FISC, :ARTIGO, :DES_OBSE, :NUM_MATR_FISC, :QTE_PONT, 
                         :DAT_EMIS_NOTF, :DAT_LIMT_RECU, :VAL_INFR, :DAT_CANC)
            ''')
            with engine.connect() as conn:
                result = conn.execute(text(sql_query), values_dict)
                if result.rowcount > 0:
                    counter = counter + 1
                conn.commit()
            engine.dispose()
            return counter
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir o auto de infração no banco de dados', 500)


@deprecated("use insert_infracoes_xls instead")
def insert_cmn_infracoes_xls(xls):
    """Insere os autos de infração no banco de dados a partir de um arquivo XLS"""
    try:
        data_frame = pd.read_excel(xls, header=0)

    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        if 'DAT_CANC' in data_frame.columns and not data_frame['DAT_CANC'].isnull().all():
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%d/%m/%Y")

        data_frame = data_frame.drop(columns=['HORA'])
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    try:
        count = data_frame.to_sql('auto_infracao', engine, if_exists='append', index=False)
        logger.systemLog(f"INFO: {count} autos processados - {xls}")
        return count

    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {xls}', 500)
