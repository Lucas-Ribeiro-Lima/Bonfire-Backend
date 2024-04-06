from datetime import datetime
from Exceptions.CustomExceptions import ErrLogger

def HandleLog(exception: Exception):
  bonfireLogPath = 'Logs/bonfire.log'
  try:
    with open(bonfireLogPath, "a") as logFile:                
      logFile.writelines(f"\n{datetime.now()} - {exception}")
  except Exception as e:
      raise ErrLogger("Error ao salvar no arquivo de log")