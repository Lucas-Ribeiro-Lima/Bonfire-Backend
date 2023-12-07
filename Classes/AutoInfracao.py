class AutoInfracao:
    def __init__(self, veiculo, numauto, concessionaria, data, local, baselegal, codinfracao, dispositivo, descricao, observacao, agente, pontuacao, dataemissao, datalimrecurso, valormulta, linha=None, placa=None):
        self.linha = linha
        self.veiculo = veiculo
        self.placa = placa
        self.numauto = numauto
        self.concessionaria = concessionaria
        self.data = data
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

