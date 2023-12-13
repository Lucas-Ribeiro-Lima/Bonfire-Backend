class SegundaInstancia:
    def __init__(self, ata, recurso, numAuto, recorrente, resultado):
        self.recurso = recurso
        self.ata = ata
        self.numAuto = numAuto
        self.recorrente = recorrente
        self.resultado = resultado

    def toDict(self):
        return {
            'recurso' : self.recurso,
            'ata': self.ata,
            'numAuto' : self.numAuto,
            'recorrente' : self.recorrente,
            'resultado' : self.resultado
        }