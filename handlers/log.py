from flask import Request
from typing import Callable

from datetime import datetime
from math import floor

class AnsiCodeFormatter:
    def __init__(self) -> None:
        self.color = {
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34"
        }
        return

    def blue(self, msg: str) -> str:
        return self.format(msg, "blue")

    def yellow(self, msg: str) -> str:
        return self.format(msg, "yellow")

    def red(self, msg: str) -> str:
        return self.format(msg, "red") 

    def green(self, msg: str) -> str:
        return self.format(msg, "green")

    def format(self, msg: str, color: str) -> str:
        _value = self.color.get(color, 0)
        return f"\x1b[1;{_value}m{msg}\x1b[0m"

class Logger:
    def __init__(self) -> None:
        self.bonfireLogPath = 'log/bonfire'
        self.formatter = AnsiCodeFormatter()
        return

    def info(self, msg: str):
        self.multilineHelper(self.formatter.blue('[INFO]'), msg)

    def warn(self, msg: str | Exception):
        self.multilineHelper(self.formatter.yellow('[WARN]'), str(msg))

    def error(self, msg: str | Exception):
        self.multilineHelper(self.formatter.red('[ERROR]'), str(msg))

    def systemLog(self, msg: str | Exception):
        self.writeToLogFile(msg, "system")

    def httpLog(self, msg:str | Exception):
        self.writeToLogFile(msg, "http")

    def writeToLogFile(self, message: str | Exception, file: str):
      """Realiza a gravação de mensagem no arquivo de log"""
      try:
        date = datetime.now()
        file_path = f"{self.bonfireLogPath}-{file}"

        with open(self.concatenateLogFileName(file_path, date), "a") as logFile:
          logFile.writelines(f"{date.strftime('%H:%M:%S')} - {message}\n")

      except Exception as _:
            print("WARN:: Error ao salvar no arquivo de log")

    def concatenateLogFileName(self, path: str, date: datetime):
        return f"{path}-{date.strftime('%d-%m-%Y')}.log"

    def multilineHelper(self, prefix: str, msg: str):
        for line in msg.splitlines():
            print(f"{prefix} {line}")

class HttpLogger(Logger):
    def __init__(self) -> None:
        super().__init__()
        self._httpFormat: dict[int, Callable[[str], str]] = {
            2: self.formatter.green,
            3: self.formatter.blue,
            4: self.formatter.red
        }

    def request(self, request: Request, status_code: int):
        ip = request.remote_addr
        method = request.method
        path = request.path

        prefix = f"[{method}] request to {path} status {status_code}:"
        suffix = f"from {ip}"

        self.format(prefix, suffix, status_code)
        self.httpLog(f"{prefix} {suffix}")

    def format(self, prefix: str, suffix: str, status: int):
       _status_rounded = floor(status / 100)
       _format_fn = self._httpFormat[_status_rounded]
       print(f"{_format_fn(prefix)} {suffix}")


logger = Logger()
http_logger = HttpLogger()
