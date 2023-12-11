from Classes.Extractor import Extractor
from Classes.Repositorio import Repositorio

def main():
    pdf_path = 'Testes\\Autos completo.pdf'
   
    try:
        auto_infracao_list =  Extractor.parse_pdf(pdf_path)
        repositorio = Repositorio();
        for auto_infracao_data in auto_infracao_list:
            repositorio.insert_auto_infracao(auto_infracao_data)

    except Exception as e:
        print(f"Um erro ocorreu: {e}")

    finally:
        repositorio.close_connection()

if __name__ == "__main__":
    main()
