#!/bin/bash
set -e

export PATH="/opt/venv/bin:/workspaces/airflow/.local/bin:${PATH}"

LOG_FILE="/tmp/init-airflow.log"

# Limpa o arquivo de log no início
echo "🔧 Iniciando Airflow standalone..." | tee $LOG_FILE

# Roda o standalone em background
airflow standalone >> $LOG_FILE 2>&1 &

# Espera o banco inicializar
sleep 10

echo "🔧 Atualizando senha do usuário admin..." | tee -a $LOG_FILE

airflow users reset-password \
    --username "$AIRFLOW_ADMIN_USER" \
    --password "$AIRFLOW_ADMIN_PASSWORD" >> $LOG_FILE 2>&1 || echo "Erro ao atualizar senha do admin" | tee -a $LOG_FILE

echo "⚙️ Configurando variáveis do Airflow..." | tee -a $LOG_FILE

if ! airflow variables get B3_DOWNLOAD_ALL >/dev/null 2>&1; then
    airflow variables set B3_DOWNLOAD_ALL "true" >> $LOG_FILE 2>&1 || { echo "Erro ao criar variável B3_DOWNLOAD_ALL" | tee -a $LOG_FILE; exit 1; }
    echo "✅ Variável B3_DOWNLOAD_ALL criada com valor 'true'!" | tee -a $LOG_FILE
else
    echo "👤 Variável B3_DOWNLOAD_ALL já existe!" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo "🔐 Airflow configurado com sucesso!" | tee -a $LOG_FILE

# Exibe informações de acesso
echo "🔗 Acesse a interface web em: http://localhost:8080" | tee -a $LOG_FILE
echo "👤 Usuário: $AIRFLOW_ADMIN_USER" | tee -a $LOG_FILE
echo "🔑 Senha: $AIRFLOW_ADMIN_PASSWORD" | tee -a $LOG_FILE