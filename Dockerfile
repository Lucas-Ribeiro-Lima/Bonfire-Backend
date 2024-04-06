FROM python:3.10-alpine

WORKDIR /

COPY . /app

WORKDIR /app

# Instalação das dependências do projeto
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]