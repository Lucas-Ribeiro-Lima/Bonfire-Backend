import PyPDF2
from Interfaces.Extractor import Extractor
from Classes.AutoInfracao import AutoInfracao
from Classes.Repositorio import Repositorio

def main():
    pdf_path = 'Testes\\Autos completo.pdf'
    auto_infracao_list = []
    repositorio = Repositorio();

    
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Cria a instância da classe AutoInfracao usando os valores extraídos
            auto_infracao = AutoInfracao(**Extractor.extrair_kvp(text))

            # Adiciona à lista
            auto_infracao_list.append(auto_infracao.to_dict())

    try:
        for auto_infracao_data in auto_infracao_list:
            repositorio.insert_auto_infracao(auto_infracao_data)

    except Exception as e:
        print(f"Um erro ocorreu: {e}")

    finally:
        repositorio.close_connection()

if __name__ == "__main__":
    main()
