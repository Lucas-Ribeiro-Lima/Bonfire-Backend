from datetime import datetime   

class Conversores:

     # converte string de data e hora em formato datetime
    def converte_data(data, hora = '00:00'):
            data_hora = f"{data} {hora}"
            data_formato = "%d/%m/%Y %H:%M"
            data_completa = datetime.strptime(data_hora, data_formato)
            data_completa = data_completa.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
            return data_completa

    def converte_float(string):
        new_string = string.replace(",", ".")
        new_string = float(new_string)
        return new_string

    def converte_dinheiro(string):
        new_string = string.replace("R$", "")
        new_string = new_string.replace(",", ".")
        new_string = float(new_string)
        return new_string

    def remove_newline(string):
        new_string = string.replace("\n", "")
        return new_string