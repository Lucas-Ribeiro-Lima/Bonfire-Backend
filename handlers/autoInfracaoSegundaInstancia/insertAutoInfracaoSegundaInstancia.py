from Classes import *
import database.mySQL as mySQL  
from sqlalchemy import text
from Exceptions.CustomExceptions import ErrNullInsert, ErrInsertDb

def insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList):
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    counter = 0
    query = "INSERT IGNORE INTO segundaInstancia (NUM_AI, NUM_ATA, NUM_RECURSO, NOM_CONC, RESULTADO, DAT_PUBL) VALUES (:NUM_AI, :NUM_ATA, :NUM_RECURSO, :NOM_CONC, :RESULTADO, :DAT_PUBL)"
    
    try:
        if autoSegundaInstanciaList == None:
            raise ErrNullInsert('Lista de auto vazio, nenhum registro inserido', 0)
        with engine.connect() as connection:
            for autoSegundaInstancia in autoSegundaInstanciaList:
                result = connection.execute(text(query), autoSegundaInstancia)
                if result.rowcount > 0:
                    counter = counter +1                   
                connection.commit()

    except Exception:
        with open("E:\\Projetos\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"problema ao realizar o insert da segunda instancia"
            print(err, file=t)
            raise ErrInsertDb(err, counter)
        
    engine.dispose()
    return counter
