# Usar uma imagem oficial do Python como base
FROM python:3.10

# Instalar wkhtmltopdf e dependências necessárias
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libxext6 \
    libjpeg62-turbo \
    xfonts-base \
    xfonts-75dpi \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt-get install -f -y && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]
