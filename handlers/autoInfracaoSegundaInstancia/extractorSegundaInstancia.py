import re
from docx import Document
from Classes.AutoSegundaInstancia import SegundaInstancia

def parseDocx(doc):

    doc = Document(doc)

    autoSegundaInstanciaList = []
    count = 0
    
    for table in doc.tables:
        for row in table.rows:


            rowData = [cell.text.strip() for cell in row.cells]

            #Formatando o número da ata/recurso
            matchAta = re.match(r'([^/]+)/(.*$)', rowData[0])
            ata = matchAta.group(1).strip() if matchAta else None
            recurso = matchAta.group(2).strip() if matchAta else None
            #Formatando o número do auto
            numAuto = rowData[1].replace("-", "").strip()
            recorrente = rowData[2]
            resultado = rowData[3]

            if ata == None:
                continue

            autoSegundaInstancia = SegundaInstancia(ata, recurso, numAuto, recorrente, resultado)    
            autoSegundaInstanciaList.append(autoSegundaInstancia.toDict())
    
    return autoSegundaInstanciaList