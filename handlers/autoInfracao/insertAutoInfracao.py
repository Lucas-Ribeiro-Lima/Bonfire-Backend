import database.sqlServer as sqlServer
from flask import jsonify, request
from Classes import *
from handlers.autoInfracao import extractor
  

def insertAutoInfracao(self, autoInfracao):
    try:
        conn = sqlServer.sqlServer()
        query = '''
            INSERT INTO auto_infracao (
                linha, veiculo, placa, num_auto, concessionaria, data, local,
                base_legal, cod_infracao, dispositivo, descricao, observacao, agente,
                pontuacao, data_emissao, data_lim_recurso, valor_multa
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''


        conn.connection.cursor.execute(query, autoInfracao.values)

        # Commit the transaction
        conn.connection.commit()
        conn.closeConnection()

    except Exception as e:   
        conn.closeConnection()
        return jsonify({"error": f"Um erro ocorreu: {e}"}), 500


