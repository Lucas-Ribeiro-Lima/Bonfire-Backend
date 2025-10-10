from datetime import datetime
from exceptions.CustomExceptions import ErrLogger

def HandleErrorLog(exception: Exception):
  """Realiza a gravação da stack completa de erros no arquivo de log"""
  bonfireLogPath = 'Logs/bonfire-error.log'
  try:
    date_str = datetime.now()
    print(f"\n{date_str} - {exception}")
    with open(bonfireLogPath, "a") as logFile:                
      logFile.writelines(f"\n{date_str} - {exception}")
  except Exception as e:
      raise ErrLogger("Error ao salvar no arquivo de log", 500)
  
def HandleSuccessLog(message: str):
  """Realiza a gravação de mensagens de sucesso no arquivo de log"""
  bonfireLogPath = 'Logs/bonfire-sucess.log'
  try:
    date_str = datetime.now()
    print(f"\n{date_str} - {message}")
    with open(bonfireLogPath, "a") as logFile:                
      logFile.writelines(f"\n{date_str} - {message}")
  except Exception as e:
      raise ErrLogger("Error ao salvar no arquivo de log", 500)