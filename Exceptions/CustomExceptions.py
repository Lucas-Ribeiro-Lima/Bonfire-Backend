
from abc import abstractmethod

class CustomException(Exception):
    @abstractmethod
    def __init__(self, message, error) -> {object}:
        self.error = error
        self.message = message
        self.counter = None
    
    def toJson(self) -> {object}:
        return {
            "error": self.error,
            "message": self.message
        }

class ErrDataPubli(CustomException):
    def __init__(self, message, error="DAT_PUBL Invalida") -> object:
        super().__init__(error, message)

    def toJson(self) -> object:
        return super().toJson()

class ErrNullInsert(CustomException):
    def __init__(self, message, error="autoSegundaInstanciaList NULL") -> object:
        super().__init__(error, message)

    def toJson(self) -> object:
        return super().toJson()

class ErrInsertDb(CustomException):
    def __init__(self, message, error="InsertAutoInfracaoSegundaIsntancia ERROR") -> object:
        super().__init__(error, message)

    def toJson(self) -> object:
        return super().toJson()
    
class ErrInvalidDbConfig(CustomException):
    def __init__(self, message, error="Invalid DB config") -> object:
        super().__init__(error, message)

    def toJson(self) -> object:
        return super().toJson()
    
class ErrCreatingDbConnection(CustomException):
    def __init__(self, message, error="Error creating DB Connection") -> object:
        super().__init__(error, message)
    
    def toJson(self) -> object:
        return super().toJson()
    
    
class ErrGetVehicles(CustomException):
    def __init__(self, message, error="Error getting vehicles") -> object:
        super().__init__(error, message)
    
    def toJson(self) -> object:
        return super().toJson()    

class ErrInsertVehicles(CustomException):
    def __init__(self, message, error="Error inserting vehicles") -> object:
        super().__init__(message, error)

    def toJson(self) -> object:
        return super().toJson()
class ErrUpdateVehicles(CustomException):
    def __init__(self, message, error="Error updating vehicles") -> object:
        super().__init__(message, error)

    def toJson(self) -> object:
        return super().toJson()
    
class ErrLogger(CustomException):
    def __init__(self, message, error="Error on logs") -> object:
        super().__init__(message, error)
    
    def toJson(self) -> object:
        return super().toJson()    
    
