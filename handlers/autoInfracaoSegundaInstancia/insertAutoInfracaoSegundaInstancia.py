from Classes import *
  

def insertAutoInfracaoSegundaInstancia(autoInfracao):
    conn = sqlServer.sqlServer()
    query = '''
        INSERT INTO segundaInstancia (
            numAuto, ata, recurso, recorrente, resultado
        )
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor = conn.connection.cursor()
    count = 0
    for i, item in enumerate(autoInfracao):
        cursor.execute(query, autoInfracao[i]["numAuto"], autoInfracao[i]["ata"], autoInfracao[i]["recurso"], autoInfracao[i]["recorrente"],
        autoInfracao[i]["resultado"])
        count = count + 1
    conn.connection.commit()
    conn.connection.close()
    return count
