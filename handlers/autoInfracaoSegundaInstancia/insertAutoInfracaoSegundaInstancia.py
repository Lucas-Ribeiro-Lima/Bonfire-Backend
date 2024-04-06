from Classes import *
import Database.databases as databases  
from sqlalchemy import text
from Exceptions.CustomExceptions import ErrNullInsert, ErrInsertDb, ErrCreatingDbConnection

def insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList):
    engine = databases.mySQL()
    engine = engine.createDatabaseStringConnection()
    counter = 0
    query = "INSERT IGNORE INTO segundaInstancia (NUM_AI, NUM_ATA, NUM_RECURSO, NOM_CONC, RESULTADO, DAT_PUBL) VALUES (:NUM_AI, :NUM_ATA, :NUM_RECURSO, :NOM_CONC, :RESULTADO, :DAT_PUBL)"
    
    if autoSegundaInstanciaList == None:
        raise ErrNullInsert('Lista de auto vazio, nenhum registro inserido', 0)

    try:
        with engine.connect() as connection:
            for autoSegundaInstancia in autoSegundaInstanciaList:
                result = connection.execute(text(query), autoSegundaInstancia)
                if result.rowcount > 0:
                    counter = counter +1                   
                connection.commit()

    except Exception:
        with open("C:\\Users\\lucas.lima\\Documents\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"Erro ao realizar o insert da segunda instancia"
            print(err, file=t)
            raise ErrInsertDb(err, counter)
        
    engine.dispose()
    return counter
