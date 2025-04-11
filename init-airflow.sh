#!/bin/bash
set -e

export PATH="/opt/venv/bin:/home/airflow/.local/bin:${PATH}"

echo "🔧 Configurando Airflow..." > /tmp/init-airflow.log 2>&1

# Verifica se o usuário já existe
echo "👤 Verificando usuário admin..." >> /tmp/init-airflow.log 2>&1
if ! airflow users list | grep -q "admin"; then
    echo "Criando usuário admin..." >> /tmp/init-airflow.log 2>&1
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname Dev \
        --role Admin \
        --email admin@example.com \
        --password admin >> /tmp/init-airflow.log 2>&1 || { echo "Erro ao criar usuário admin" >> /tmp/init-airflow.log; exit 1; }
    echo "✅ Usuário admin criado com sucesso!" >> /tmp/init-airflow.log 2>&1
else
    echo "👤 Usuário admin já existe!" >> /tmp/init-airflow.log 2>&1
fi

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