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
    cursor = conn.connection.cursor()
    count = 0
    for i, item in enumerate(autoInfracao):
        cursor.execute(query, autoInfracao[i]["linha"], autoInfracao[i]["veiculo"], autoInfracao[i]["placa"], autoInfracao[i]["numauto"],
        autoInfracao[i]["concessionaria"], autoInfracao[i]["data"], autoInfracao[i]["local"], autoInfracao[i]["baselegal"],
        autoInfracao[i]["codinfracao"], autoInfracao[i]["dispositivo"], autoInfracao[i]["descricao"], autoInfracao[i]["observacao"],
        autoInfracao[i]["agente"], autoInfracao[i]["pontuacao"], autoInfracao[i]["dataemissao"], autoInfracao[i]["datalimrecurso"],
        autoInfracao[i]["valormulta"])
        count = count + 1
    conn.connection.commit()
    conn.connection.close()
    return count
