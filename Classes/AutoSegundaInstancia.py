class SegundaInstancia:
    def __init__(self, NUM_ATA, NUM_RECURSO, NUM_AI, NOM_CONC, RESULTADO):
        self.recurso = NUM_RECURSO
        self.ata = NUM_ATA
        self.numAuto = NUM_AI
        self.recorrente = NOM_CONC
        self.resultado = RESULTADO

    def toDict(self):
        return {
            'NUM_RECURSO' : self.recurso,
            'NUM_ATA': self.ata,
            'NUM_AI' : self.numAuto,
            'NOM_CONC' : self.recorrente,
            'RESULTADO' : self.resultado
        }