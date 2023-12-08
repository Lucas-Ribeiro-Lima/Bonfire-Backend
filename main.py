import PyPDF2
import json
import pyodbc
from Interfaces.Extractor import Extractor
from Classes.AutoInfracao import AutoInfracao

def main():
    pdf_path = 'Testes/Autos completo.pdf'
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

    conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=192.168.0.11,32772;'
                        'DATABASE=bonfire;'
                        'UID=sa;'
                        'PWD=teste12345')

    for i, item in enumerate(auto_infracao_list):

        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO auto_infracao (
                linha, veiculo, placa, num_auto, concessionaria, data, local,
                base_legal, cod_infracao, dispositivo, descricao, observacao, agente,
                pontuacao, data_emissao, data_lim_recurso, valor_multa
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        json_data[i]['linha'], json_data[i]['veiculo'], json_data[i]['placa'], json_data[i]['numauto'],
        json_data[i]['concessionaria'], json_data[i]['data'], json_data[i]['local'],
        json_data[i]['baselegal'], json_data[i]['codinfracao'], json_data[i]['dispositivo'],
        json_data[i]['descricao'], json_data[i]['observacao'], json_data[i]['agente'],
        json_data[i]['pontuacao'], json_data[i]['dataemissao'], json_data[i]['datalimrecurso'],
        json_data[i]['valormulta'])

        # Commit the transaction
        conn.commit()

    # Close the connection
    conn.close() 

if __name__ == "__main__":
    main()
