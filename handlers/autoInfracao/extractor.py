import re
import PyPDF2
from Classes.AutoInfracao import AutoInfracao
from Classes.Conversores import Conversores

class Extractor:

    # Lógica para identificar as KVP
    def extractKVP(text):
        veiculo_match = re.findall(r'(Veículo: (\w+))', text)
        linha_match = re.findall(r'(Linha: (\w+))', text)
        placa_match = re.findall(r'(Placa: (\w+))', text)
        numauto_match = re.findall(r'(Auto de Infração: (\w+))', text)
        concessionaria_match = re.findall(r'(Concessionária: (\w.+))', text)
        data_match = re.findall(r'(Data:(\d{2}/\d{2}/\d{4}))', text)
        hora_match = re.findall(r'(Hora:(\d{2}:\d{2}))', text)
        local_match = re.findall(r'(Local: (\w.+))', text)
        baselegal_match = re.findall(r'(Base Legal: (\w.+))', text)
        codinfracao_match = re.findall(r'(Cód. Infração: (\w+))', text)
        dispositivo_match = re.findall(r'(Dispositivo: (\w.+))', text)
        descricao_match = re.findall(r'(Descrição da Infração: (\w.+))', text)
        observacao_match = re.findall(r'(Observação: (\w.+))', text)
        agente_match = re.findall(r'(Identificação do Agente: (\w+))', text)
        pontuacao_match = re.findall(r'(Pontuação: (\d+,\d*))', text)
        dataemissao_match = re.findall(r'(Data de Emissão: (\d{2}/\d{2}/\d{4}))', text)
        datalimrecurso_match = re.findall(r'(Data Limite Recurso: (\w.+))', text)
        valormulta_match = re.findall(r'(Valor da Multa: (\w.+))', text)

        # Atribuindo o primeiro valor capturado pelo regex a variavel que será utilizada para construir o objeto
        
        veiculo = int(veiculo_match[0][1]) if veiculo_match and veiculo_match[0][1].isdigit() else None
        linha = linha_match[0][1] if linha_match else None
        placa = placa_match[0][1] if placa_match else None
        numauto = numauto_match[0][1] if numauto_match else None
        concessionaria = concessionaria_match[0][1] if concessionaria_match else None

        data = data_match[0][1] if data_match else None
        hora = hora_match[0][1] if hora_match else None
        data_hora = Conversores.converte_data(data, hora)

        local = local_match[0][1] if local_match else None
        baselegal = baselegal_match[0][1] if baselegal_match else None
        codinfracao = int(codinfracao_match[0][1] if codinfracao_match else None)
        dispositivo = Conversores.remove_espaco(dispositivo_match[0][1] if dispositivo_match else None)
        descricao = descricao_match[0][1] if descricao_match else None
        observacao = observacao_match[0][1] if observacao_match else None
        agente = int(agente_match[0][1] if agente_match else None)
        pontuacao = Conversores.converte_float(pontuacao_match[0][1] if pontuacao_match else None)
        dataemissao = Conversores.converte_data(dataemissao_match[0][1] if dataemissao_match else None)
        datalimrecurso = Conversores.converte_data(datalimrecurso_match[0][1] if datalimrecurso_match else None)
        valormulta = Conversores.converte_dinheiro(valormulta_match[0][1] if valormulta_match else None)

        return {
            'linha': linha,
            'veiculo': veiculo,
            'placa': placa,
            'numauto': numauto,
            'concessionaria': concessionaria,
            'data': data_hora,
            'local': local,
            'baselegal': baselegal,
            'codinfracao': codinfracao,
            'dispositivo': dispositivo,
            'descricao': descricao,
            'observacao': observacao,
            'agente': agente,
            'pontuacao': pontuacao,
            'dataemissao': dataemissao,
            'datalimrecurso': datalimrecurso,
            'valormulta': valormulta
        }

def parsePdf(pdf):

    auto_infracao_list = []

    pdf_reader = PyPDF2.PdfReader(pdf)
    count = 0
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Cria a instância da classe AutoInfracao usando os valores extraídos
        auto_infracao = AutoInfracao(**Extractor.extractKVP(text))

        # Adiciona à lista
        auto_infracao_list.append(auto_infracao.to_dict())
        count = count +1

    return auto_infracao_list, count