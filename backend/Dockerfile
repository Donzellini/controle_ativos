FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar os requisitos primeiro (otimização de cache)
COPY requirements.txt .

# INSTALAÇÃO CRUCIAL: Instala as dependências e o pacote que o log exige
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "fastapi[standard]"

# Copiar o resto do código da pasta backend
COPY . .

# Expor a porta
EXPOSE 8000

# COMANDO SEGURO: Usar o uvicorn diretamente evita que o Fly tente usar o CLI que está a falhar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]