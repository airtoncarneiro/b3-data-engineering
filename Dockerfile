FROM apache/airflow:2.10.5

# Instalar dependências do requirements.txt, se houver
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

USER root
# Criar o grupo airflow e ajustar o usuário para AIRFLOW_UID
ARG AIRFLOW_UID=50000
RUN groupadd -g ${AIRFLOW_UID} airflow && \
    usermod -u ${AIRFLOW_UID} -g ${AIRFLOW_UID} airflow && \
    chown -R airflow:airflow /home/airflow /opt/airflow

USER airflow