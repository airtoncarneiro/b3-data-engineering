#!/bin/bash
set -e

export PATH="/opt/venv/bin:/workspaces/airflow/.local/bin:${PATH}"

echo "🔧 Iniciando Airflow standalone..." > /tmp/init-airflow.log 2>&1

# Roda o standalone em background
airflow standalone >> /tmp/init-airflow.log 2>&1 &

# Espera o banco inicializar
sleep 10

echo "🔧 Atualizando senha do usuário admin..." >> /tmp/init-airflow.log 2>&1

airflow users reset-password \
    --username admin \
    --password admin >> /tmp/init-airflow.log 2>&1 || echo "Erro ao atualizar senha do admin" >> /tmp/init-airflow.log

# airflow users reset-password \
#     --username "${AIRFLOW_ADMIN_USER}" \
#     --password "${AIRFLOW_ADMIN_PASSWORD}" >> /tmp/init-airflow.log 2>&1 || echo "Erro ao atualizar senha do admin" >> /tmp/init-airflow.log



# Cria a variável B3_DOWNLOAD_ALL se ela não existir
echo "⚙️ Configurando variáveis do Airflow..." >> /tmp/init-airflow.log 2>&1
if ! airflow variables get B3_DOWNLOAD_ALL >/dev/null 2>&1; then
    airflow variables set B3_DOWNLOAD_ALL "true" >> /tmp/init-airflow.log 2>&1 || { echo "Erro ao criar variável B3_DOWNLOAD_ALL" >> /tmp/init-airflow.log; exit 1; }
    echo "✅ Variável B3_DOWNLOAD_ALL criada com valor 'true'!" >> /tmp/init-airflow.log 2>&1
else
    echo "👤 Variável B3_DOWNLOAD_ALL já existe!" >> /tmp/init-airflow.log 2>&1
fi

echo -e "✅ Configuração concluída." >> /tmp/init-airflow.log 2>&1
cat /tmp/init-airflow.log
