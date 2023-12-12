class SegundaInstancia:
    def __init__(ata, dv, recorrente, resultado):
        self.ata = ata
        self.dv = dv
        self.recorrente = recorrente
        self.resultado = resultado

    def toDict(self):
        return {
            'ata': self.ata,
            'dv' : self.dv,
            'recorrente' : self.recorrente,
            'resultado' : self.resultado
        }