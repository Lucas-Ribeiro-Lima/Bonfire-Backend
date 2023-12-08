import PyPDF2
import json
import pyodbc
from Interfaces.Extractor import Extractor
from Classes.AutoInfracao import AutoInfracao

def main():
    pdf_path = 'Testes\\Autos completo.pdf'
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

    conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=192.168.0.1;'
                        'DATABASE=bonfire;'
                        'UID=sa;'
                        'PWD=password')

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

        auto_infracao_list[i]["linha"], auto_infracao_list[i]["veiculo"], auto_infracao_list[i]["placa"], auto_infracao_list[i]["numauto"],
        auto_infracao_list[i]["concessionaria"], auto_infracao_list[i]["data"], auto_infracao_list[i]["local"], auto_infracao_list[i]["baselegal"],
        auto_infracao_list[i]["codinfracao"], auto_infracao_list[i]["dispositivo"], auto_infracao_list[i]["descricao"], auto_infracao_list[i]["observacao"],
        auto_infracao_list[i]["agente"], auto_infracao_list[i]["pontuacao"], auto_infracao_list[i]["dataemissao"], auto_infracao_list[i]["datalimrecurso"],
        auto_infracao_list[i]["valormulta"])

        # Commit the transaction
        conn.commit()

    # Close the connection
    conn.close() 

if __name__ == "__main__":
    main()
