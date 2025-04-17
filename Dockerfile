# Usar uma imagem oficial do Python como base
FROM python:3.10

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxrender1 \
    libfontconfig1 \
    libxext6 \
    libx11-6 \
    && apt-get clean
# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]