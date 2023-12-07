import PyPDF2
import json
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
    json_data = json.dumps(auto_infracao_list, indent=2, ensure_ascii=False)
    print(json_data)


if __name__ == "__main__":
    main()
