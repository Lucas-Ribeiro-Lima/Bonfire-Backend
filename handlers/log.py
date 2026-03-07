from datetime import datetime

bonfireLogPath = 'log/bonfire.log'
  
def writeToLogFile(message: str | Exception):
  """Realiza a gravação de mensagem no arquivo de log"""
  try:
    date_str = datetime.now()
    print(f"{date_str} - {message}")
    with open(bonfireLogPath, "a") as logFile:                
      logFile.writelines(f"{date_str} - {message}\n")

  except Exception as _:
        print("WARN:: Error ao salvar no arquivo de log")
