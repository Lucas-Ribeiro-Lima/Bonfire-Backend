from flask import jsonify, request
from Classes import *
from database import mySQL as mySQL
from sqlalchemy import text

def deleteVeiculos(veiculos):
    # Extrai os dados do veiculo
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    query = '''DELETE FROM veiculos WHERE num_veiculo = :num_veiculo AND placa = :placa'''
    counter = 0    
    try: 
        with engine.connect() as connection:
            for i in veiculos:
                result = connection.execute(text(query), i)
                if result.rowcount > 0:
                    counter = counter +1
            connection.commit()
        

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"ERRO: problema ao realizar o delete dos veículos"
            return err, e
        
    engine.dispose()
    return counter, None
