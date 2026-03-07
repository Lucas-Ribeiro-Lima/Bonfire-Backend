from datetime import datetime

bonfireLogPath = 'log/bonfire'

def concatenateLogFileName(date: datetime):
    return f"{bonfireLogPath}-{date.strftime("%d-%m-%Y")}.log"
  
def writeToLogFile(message: str | Exception):
  """Realiza a gravação de mensagem no arquivo de log"""
  try:
    date = datetime.now()
    print(f"{date.strftime('%d-%m-%Y %H:%M:%S')} - {message}")
    with open(concatenateLogFileName(date), "a") as logFile:
      logFile.writelines(f"{date.strftime('%H:%M:%S')} - {message}\n")

  except Exception as _:
        print("WARN:: Error ao salvar no arquivo de log")
