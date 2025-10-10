class Recurso:
    def __init__(self, NUM_ATA, NUM_RECURSO, NUM_AI, NOM_CONC, RESULTADO, DAT_PUBL):
        self.recurso = NUM_RECURSO
        self.ata = NUM_ATA
        self.numAuto = NUM_AI
        self.recorrente = NOM_CONC
        self.resultado = RESULTADO
        self.dat_publ = DAT_PUBL

    def toDict(self):
        return {
            'NUM_RECURSO' : self.recurso,
            'NUM_ATA': self.ata,
            'NUM_AI' : self.numAuto,
            'NOM_CONC' : self.recorrente,
            'RESULTADO' : self.resultado,
            'DAT_PUBL' : self.dat_publ
        }