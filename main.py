import PyPDF2
import json
from Interfaces.Extractor import Extractor
from Classes.AutoInfracao import AutoInfracao
import pyodbc

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
   
    # Connect to SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=192.168.0.11,32771;'
                        'DATABASE=bonfire;'
                        'UID=sa;'
                        'PWD=teste12345')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO auto_infracao (
            linha, veiculo, placa, num_auto, concessionaria, data, local,
            base_legal, cod_infracao, dispositivo, descricao, observacao, agente,
            pontuacao, data_emissao, data_lim_recurso, valor_multa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', 
    json_data[0]['linha'], json_data[0]['veiculo'], json_data[0]['placa'], json_data[0]['numauto'],
    json_data[0]['concessionaria'], json_data[0]['data'], json_data[0]['local'],
    json_data[0]['baselegal'], json_data[0]['codinfracao'], json_data[0]['dispositivo'],
    json_data[0]['descricao'], json_data[0]['observacao'], json_data[0]['agente'],
    json_data[0]['pontuacao'], json_data[0]['dataemissao'], json_data[0]['datalimrecurso'],
    json_data[0]['valormulta'])

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
