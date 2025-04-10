FROM apache/airflow:2.10.5
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

USER root
# Criar o grupo airflow e ajustar o usuário
RUN groupadd -g 1000 airflow && \
    usermod -u 1000 -g 1000 airflow && \
    chown -R airflow:airflow /home/airflow

USER airflow