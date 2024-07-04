class CustomException(Exception):
    """Classe básica para as exceções customizadas da aplicação"""
    def __init__(self,  message: str, status: int = 500, error:  str = '') -> None:
        self.error = error
        self.message = message
        self.status = status
        self.counter = None
    
    def to_json(self) -> dict:
        return {
            "error": self.error,
            "message": self.message,
            "status": self.status,
        }

class ErrDataPubli(CustomException):
    def __init__(self, message, status, error="DAT_PUBL Invalida"):
        super().__init__(message, status, error)

class ErrNullInsert(CustomException):
    def __init__(self, message, status, error="autoSegundaInstanciaList NULL"):
        super().__init__(message, status, error)
    
class ErrInvalidDbConfig(CustomException):
    def __init__(self, message, status, error="Invalid DB config"):
        super().__init__(message, status, error)
    
class ErrCreatingDbConnection(CustomException):
    def __init__(self, message, status, error="Error creating DB Connection"):
        super().__init__(message, status, error)

class ErrGetData(CustomException):
    def __init__(self, message, status, error="Error fetching data"):
        super().__init__(message, status, error)
    
class ErrInsertData(CustomException):
    def __init__(self, message, status, error="Error inserting data"):
        super().__init__(message, status, error)
        
class ErrUpdateData(CustomException):
    def __init__(self, message, status, error="Error updating data"):
        super().__init__(message, status, error)

class ErrIncompleteData(CustomException):
    def __init__(self,  message, status, error="Incomplete Data"):
        super().__init__(message, status, error)
    
class ErrLogger(CustomException):
    def __init__(self, message, status, error="Error on logs"):
        super().__init__(message, status, error)       
        
class ErrInvalidJson(CustomException):
    def __init__(self, expectedObject, message, status, error="Invalid JSON Object"):
        super().__init__(message, status, error)
        self.expectedObject = expectedObject

    def to_json(self) -> dict:
        return {
            "error": self.error,
            "message": self.message,
            "object_expected": self.expectedObject,
        }

class ErrReadingFile(CustomException):
    def __init__(self, message: str, status: int = 500, error="Error in file"):
        super().__init__(error, message, status)


class ErrQuantityOfAtas(CustomException):
    def __init__(self, message: str, qtdAtas, qtdTables, status: int = 400, error: str ="Error extracting atas or tables"):
        super().__init__(message, status, error)
        self.qtdAtas = qtdAtas
        self.qtdTables = qtdTables

    def to_json(self) -> dict:
        return {
            "error": self.error,
            "message": self.message,
            "qtdAtas": self.qtdAtas,
            "qtdTables": self.qtdTables,
        }