from flask import jsonify, request
from Classes import *
from database import mySQL as mySQL
from sqlalchemy import text

def updateVeiculos(veiculos):
    # Extrai os dados do veiculo
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    query = '''UPDATE veiculos set VEIC_ATIV_EMPR = :VEIC_ATIV_EMPR WHERE NUM_VEIC = :NUM_VEIC'''
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
            err = f"ERRO: problema ao realizar o update dos veículos"
            return err, e
        
    engine.dispose()
    return counter, None
