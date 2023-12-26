from Classes import *
import database.mySQL as mySQL  
from sqlalchemy import text

def insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList):
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    counter = 0
    query = "INSERT INTO segundaInstancia (NUM_AI, NUM_ATA, NUM_RECURSO, NOM_CONC, RESULTADO, DAT_PUBL) VALUES (:NUM_AI, :NUM_ATA, :NUM_RECURSO, :NOM_CONC, :RESULTADO, :DAT_PUBL)"
    
    try:
        with engine.connect() as connection:
            for autoSegundaInstancia in autoSegundaInstanciaList:
                result = connection.execute(text(query), autoSegundaInstancia)
                if result.rowcount > 0:
                    counter = counter +1
                connection.commit()

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"ERRO: problema ao realizar o insert da segunda instancia"
            print(err, file=t)
            return err, e
        
    engine.dispose()
    return counter, None
