from docx import Document

def parseDocx(doc):

    doc = Document(doc)

    tableData = []
    
    for table in doc.tables:
        for row in table.rows:
            rowData = [cell.text.strip() for cell in row.cells]
            tableData.append(rowData)
            

    return tableData