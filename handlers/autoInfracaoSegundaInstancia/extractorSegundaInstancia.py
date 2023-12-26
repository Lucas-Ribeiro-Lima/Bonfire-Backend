import re
from docx import Document
from Classes.AutoSegundaInstancia import SegundaInstancia

def parseDocx(docx):

    doc = Document(docx)
    autoSegundaInstanciaList = []
    count = 0
    extracted_text = ""
    # for paragraph in doc.paragraphs:
    #     extracted_text = paragraph.text + " "

    #     matchAta = re.match(r'ATA DA (\d+)ª', extracted_text)
    #     NUM_ATA = int(matchAta.group(1))
        
    for table in doc.tables:
        for row in table.rows:
            rowData = [cell.text.strip() for cell in row.cells]

            NUM_RECURSO = rowData[0]
            NUM_AI = rowData[1]
            NOM_CONC = rowData[2]
            valida_resultado = str(rowData[3]).upper()
            if valida_resultado == 'IMPROCEDENTE':
                RESULTADO = False
            else:
                RESULTADO = True 
            NUM_ATA = 1

            if NUM_RECURSO =='RECURSO':
                continue

            autoSegundaInstancia = SegundaInstancia(NUM_ATA, NUM_RECURSO, NUM_AI, NOM_CONC, RESULTADO)  
            autoSegundaInstanciaList.append(autoSegundaInstancia.toDict())  
    
    return autoSegundaInstanciaList