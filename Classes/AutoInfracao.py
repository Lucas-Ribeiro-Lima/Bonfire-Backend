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