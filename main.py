import PyPDF2
import json
from Interfaces.Extractor import Extractor
from Classes.AutoInfracao import AutoInfracao
import pyodbc
from datetime import datetime

def main():
    pdf_path = 'Testes/Auto com veiculo.pdf'
    auto_infracao_list = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Cria a instância da classe AutoInfracao usando os valores extraídos
            auto_infracao = AutoInfracao(**Extractor.extrair_kvp(text))

            # Adiciona à lista
            auto_infracao_list.append(auto_infracao.to_dict())

    # Converte para JSON
    json_dump = json.dumps(auto_infracao_list, indent=2, ensure_ascii=False, default=str)
    json_data = json.loads(json_dump)
    print(json_data[])
   
   
    # Connect to SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=172.22.0.15;'
                        'DATABASE=bonfire;'
                        'UID=sa;'
                        'PWD=G@.BD@2018%!')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO auto_infracao (
            linha, veiculo, placa, numauto, concessionaria, data, local,
            baselegal, codinfracao, dispositivo, descricao, observacao, agente,
            pontuacao, dataemissao, datalimrecurso, valormulta
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', 
    json_data[0], json_data[1], json_data[2], json_data[3],
    json_data[4], json_data[5],
    json_data[6], json_data[7], json_data[8],
    json_data[9], json_data[10], json_data[11],
    json_data[12], json_data[13],
    json_data[14], json_data[15], json_data[17])

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
