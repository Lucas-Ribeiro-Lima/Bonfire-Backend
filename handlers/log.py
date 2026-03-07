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


class Logger:
    def multilineHelper(self, prefix: str, msg: str):
        for line in msg.splitlines():
            print(f"{prefix} {line}")

    def info(self, msg: str):
        prefix = "\x1b[34m[INFO]\x1b[0m"
        self.multilineHelper(prefix, msg)

    def warn(self, msg: str | Exception):
        print(f"\x1b[33m[WARN]\x1b[0m {msg}")

    def error(self, msg: str | Exception):
        print(f"\x1b[31m[ERROR]\x1b[0m {msg}")

    def raw(self, msg:str):
        print(msg)

logger = Logger()

