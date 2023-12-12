import database.sqlServer as sqlServer
from flask import jsonify, request
from Classes import *

def postVeiculo(veiculos):
    try:
        # Extrai os dados do veiculo
        dadosVeiculo = veiculos["veiculo"]
        veiculo = Veiculo(num_veiculo=dadosVeiculo["num_veiculo"], placa=dadosVeiculo["placa"])

        # Cria uma instância do Repositorio e insere o veículo
        conn = sqlServer.sqlServer()
        query = '''
            INSERT INTO veiculos (
                num_veiculo, placa
            )
            VALUES (?,?)
        '''       
        conn.connection.cursor.execute(query, tuple(veiculo.values()))
        
        conn.connection.commit()
        sqlServer.closeConnection()
        

    except Exception:
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500
