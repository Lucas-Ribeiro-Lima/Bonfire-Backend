import PyPDF2
import re
import json

class AutoInfracao:
    def __init__(self, veiculo, numauto, concessionaria, data, hora, local, baselegal, codinfracao, dispositivo, descricao, observacao, agente, pontuacao, dataemissao, datalimrecurso, valormulta, linha=None, placa=None):
        self.linha = linha
        self.veiculo = veiculo
        self.placa = placa
        self.numauto = numauto
        self.concessionaria = concessionaria
        self.data = data
        self.hora = hora
        self.local = local
        self.baselegal = baselegal
        self.codinfracao = codinfracao
        self.dispositivo = dispositivo
        self.descricao = descricao
        self.observacao = observacao
        self.agente = agente
        self.pontuacao = pontuacao
        self.dataemissao = dataemissao
        self.datalimrecurso = datalimrecurso
        self.valormulta = valormulta

    def to_dict(self):
        # Converte os atributos da classe para um dicionário
        return {
            'linha': self.linha,
            'veiculo': self.veiculo,
            'placa': self.placa,
            'numauto': self.numauto,
            'concessionaria': self.concessionaria,
            'data': self.data,
            'hora': self.hora,
            'local': self.local,
            'baselegal': self.baselegal,
            'codinfracao': self.codinfracao,
            'dispositivo': self.dispositivo,
            'descricao': self.descricao,
            'observacao': self.observacao,
            'agente': self.agente,
            'pontuacao': self.pontuacao,
            'dataemissao': self.dataemissao,
            'datalimrecurso': self.datalimrecurso,
            'valormulta': self.valormulta
        }

    def __str__(self):
        return (f"Linha: {self.linha}, Veículo: {self.veiculo}, Placa: {self.placa}, Número do Auto: {self.numauto}, "
                f"Concessionária: {self.concessionaria}, Data: {self.data}, Local: {self.local}, Base Legal: {self.baselegal}, "
                f"Código da Infração: {self.codinfracao}, Dispositivo: {self.dispositivo}, Descrição: {self.descricao}, "
                f"Observação: {self.observacao}, Agente: {self.agente}, Pontuação: {self.pontuacao}, Data de Emissão: {self.dataemissao}, "
                f"Data Limite de Recurso: {self.datalimrecurso}, Valor da Multa: {self.valormulta}")

    def exibir(self):
        print(f"Número do Auto: {self.numauto}, Concessionária: {self.concessionaria}, Linha: {self.linha}, Veículo: {self.veiculo}, Placa: {self.placa}")
        print(f"Local: {self.local}, Base Legal: {self.baselegal}, Código da Infração: {self.codinfracao}, Dispositivo: {self.dispositivo}")
        print(f"Descrição: {self.descricao}, Observação: {self.observacao}, Agente: {self.agente}, Pontuação: {self.pontuacao}")
        print(f"Data de Emissão: {self.dataemissao}, Data Limite de Recurso: {self.datalimrecurso}, Valor da Multa: {self.valormulta}")
        print()

def extrair_kvp(pdf_path):
    auto_infracao_list = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Use len(reader.pages) para obter o número de páginas
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Lógica para identificar as KVP
            veiculo_match = re.findall(r'(Veículo: (\w+))', text)
            linha_match = re.findall(r'(Linha: (\w+))', text)
            placa_match = re.findall(r'(Placa: (\w+))', text)
            numauto_match = re.findall(r'(Auto de Infração: (\w+))', text)
            concessionaria_match = re.findall(r'(Concessionária: (\w.+))', text)
            data_match = re.findall(r'Data:(\d{2}/\d{2}/\d{4})', text)
            hora_match = re.findall(r'Hora:(\d{2}:\d{2})', text)
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
            veiculo = veiculo_match[0][1] if veiculo_match else None
            linha = linha_match[0][1] if linha_match else None
            placa = placa_match[0][1] if placa_match else None
            numauto = numauto_match[0][1] if numauto_match else None
            concessionaria = concessionaria_match[0][1] if concessionaria_match else None
            data = data_match[0][1] if data_match else None
            hora = hora_match[0][1] if hora_match else None
            local = local_match[0][1] if local_match else None
            baselegal = baselegal_match[0][1] if baselegal_match else None
            codinfracao = codinfracao_match[0][1] if codinfracao_match else None
            dispositivo = dispositivo_match[0][1] if dispositivo_match else None
            descricao = descricao_match[0][1] if descricao_match else None
            observacao = observacao_match[0][1] if observacao_match else None
            agente = agente_match[0][1] if agente_match else None
            pontuacao = pontuacao_match[0][1] if pontuacao_match else None
            dataemissao = dataemissao_match[0][1] if dataemissao_match else None
            datalimrecurso = datalimrecurso_match[0][1] if datalimrecurso_match else None
            valormulta = valormulta_match[0][1] if valormulta_match else None



            # Criar instância da classe AutoInfracao e adicioná-la à lista
            auto_infracao = AutoInfracao(veiculo, numauto, concessionaria, data, hora, local, baselegal, codinfracao, dispositivo, descricao, observacao, agente, pontuacao, dataemissao, datalimrecurso, valormulta, linha, placa)
            auto_infracao_list.append(auto_infracao.to_dict())

    return auto_infracao_list

# Exemplos de teste de output
pdf_path = 'Testes/pdf completo de infracoes.pdf'
lista_auto_infracoes = extrair_kvp(pdf_path)

json_data = json.dumps(lista_auto_infracoes, indent=2, ensure_ascii=False)

print(json_data)

