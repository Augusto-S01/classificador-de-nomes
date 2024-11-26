# Use uma imagem base do Python
FROM python:3.7.16

# Crie e defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt /app/requirements.txt
COPY data.csv /app/data.csv
COPY modeloRedeNeural.h5 /app/modeloRedeNeural.h5

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o diretório de trabalho
COPY . /app

# Exponha a porta em que o FastAPI estará ouvindo
EXPOSE 8000

# Comando para executar a aplicação com Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9999", "--reload"]
