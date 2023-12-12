import database.sqlServer as sqlServer
from flask import jsonify, request
from Classes import *
  

def insertAutoInfracao(autoInfracao):
    conn = sqlServer.sqlServer()
    query = '''
        INSERT INTO auto_infracao (
            linha, veiculo, placa, num_auto, concessionaria, data, local,
            base_legal, cod_infracao, dispositivo, descricao, observacao, agente,
            pontuacao, data_emissao, data_lim_recurso, valor_multa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    for i in autoInfracao:
        conn.connection.cursor.execute(query, [i]["linha"], [i]["veiculo"], [i]["placa"], [i]["numauto"],
        [i]["concessionaria"], [i]["data"], [i]["local"], [i]["baselegal"],
        [i]["codinfracao"], [i]["dispositivo"], [i]["descricao"], [i]["observacao"],
        [i]["agente"], [i]["pontuacao"], [i]["dataemissao"], [i]["datalimrecurso"],
        [i]["valormulta"])
        conn.connection.commit()
        conn.closeConnection()
        return i
