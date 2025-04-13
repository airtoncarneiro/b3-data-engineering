#!/bin/bash
set -e

export PATH="/opt/venv/bin:/workspaces/airflow/.local/bin:${PATH}"

LOG_FILE="/tmp/init-airflow.log"

echo "🔧 Inicializando Airflow..." | tee $LOG_FILE

# Inicializa o banco de dados do Airflow
airflow db init >> $LOG_FILE 2>&1

# Cria o usuário admin (ignora erro se já existir)
echo "🔧 Criando usuário admin..." | tee -a $LOG_FILE
airflow users create \
    --username "$AIRFLOW_ADMIN_USER" \
    --password "$AIRFLOW_ADMIN_PASSWORD" \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com >> $LOG_FILE 2>&1 || true

# Executa script auxiliar para configurar variáveis
bash /tmp/init-airflow.sh >> $LOG_FILE 2>&1

echo "🔧 Iniciando Webserver e Scheduler..." | tee -a $LOG_FILE

# Inicia webserver e scheduler em background
airflow webserver >> /tmp/webserver.log 2>&1 &
airflow scheduler >> /tmp/scheduler.log 2>&1 &

# Mantém o container rodando
wait -n

echo "Airflow finalizado."
