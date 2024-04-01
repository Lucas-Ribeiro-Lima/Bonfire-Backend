FROM python:3.10-alpine

WORKDIR /

COPY . /app

WORKDIR /app

# Instalação das dependências do projeto
RUN pip install --no-cache-dir \
    sqlalchemy \
    pandas \
    mySql \    
    Blueprint \
    Flask \
    Flask-CORS \
    waitress

EXPOSE 5000

CMD ["python", "app.py"]