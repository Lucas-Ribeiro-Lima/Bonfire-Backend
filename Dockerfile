FROM python:3.10-alpine

WORKDIR /app

COPY . .

# Instalação das dependências do projeto
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]