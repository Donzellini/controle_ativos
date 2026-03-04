# Use a imagem slim diretamente para simplificar e evitar erros de permissão no .venv
FROM python:3.12-slim

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y gcc libsqlite3-dev && rm -rf /var/lib/apt/lists/*

# Cria o virtualenv e instala as dependências
RUN python -m venv .venv
COPY requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o Fly.io espera
EXPOSE 8000

# Comando corrigido: usa o executável dentro do venv explicitamente
CMD [".venv/bin/fastapi", "run", "main.py", "--port", "8000"]