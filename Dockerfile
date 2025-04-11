# Estágio de build para dependências Python
FROM python:3.10-slim AS python-builder

# Instala apenas as dependências necessárias para build
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria e ativa ambiente virtual 
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia e instala requirements
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Estágio final
FROM python:3.10-slim

# Instala apenas as dependências de runtime
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    default-libmysqlclient-dev \
    curl \
    git \
    tmux \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    AIRFLOW_HOME=/home/airflow


# Criação do usuário e diretórios
RUN groupadd -g 1000 airflow && \
    useradd -m -u 1000 -g 1000 -s /bin/bash airflow 

# Copia o ambiente virtual do estágio de build
COPY --from=python-builder /opt/venv /opt/venv

WORKDIR /home/airflow

# Copia script de inicialização para /tmp
COPY init-airflow.sh /tmp/init-airflow.sh
RUN chmod +x /tmp/init-airflow.sh

# Define o usuário padrão
USER airflow
