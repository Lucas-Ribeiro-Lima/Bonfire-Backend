class ErrDataPubli(Exception):
    def __init__(self, message):
        self.erro = "DAT_PUBL Invalida"
        self.message = message
    
    def to_dict(self):
        return {
            "erro": self.erro, 
            "message": self.message
        }

class ErrNullInsert(Exception):
    def __init__(self, message, counter):
        self.erro = "autoSegundaInstanciaList NULL"
        self.message = message
        self.counter = counter

    def to_dict(self):
        return {
                "erro": self.erro,
                "message": self.message, 
                "counter": self.counter
            }

class ErrInsertDb(Exception):
    def __init__(self, message, counter):
        self.erro = "InsertAutoInfracaoSegundaIsntancia ERROR"
        self.message = message
        self.counter = counter

    def to_dict(self):
        return {
                "erro": self.erro, 
                "message": self.message, 
                "counter": self.counter
            }

class ErrInvalidDbConfig(Exception):
    def __init__(self, message):
        self.erro = "Invalid DB config"
        self.message = message

    def to_dict(self):
        return {
            "erro": self.erro, 
            "message": self.message
        }
    
class ErrCreatingDbConnection(Exception):
    def __init__(self, message):
        self.erro = "Error creating DB Connection"
        self.message = message

    def to_dict(self):
        return{
            "erro": self.erro,
            "message": self.message,
        }