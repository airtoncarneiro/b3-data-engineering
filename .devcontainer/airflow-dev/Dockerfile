FROM python:3.10.13-slim-bullseye

# Instala as dependências necessárias
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends build-essential libffi-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Atualiza o pip
RUN pip install --upgrade pip

ENV AIRFLOW_HOME=/workspaces/b3/airflow/

WORKDIR ${AIRFLOW_HOME}

# Define as versões do Airflow e do Python como variáveis de ambiente
ENV AIRFLOW_VERSION=2.8.2
ENV PYTHON_VERSION=3.10
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Instala o Apache Airflow com restrições de versão
RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Inicializa o banco de dados do Airflow
RUN airflow db init

# Configura o usuário inicial do Airflow
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Airton \
    --lastname Carneiro \
    --role Admin \
    --email email@email.com

# Executa as migrações do banco de dados do Airflow (opcional se você já usou db init)
# RUN airflow db upgrade
