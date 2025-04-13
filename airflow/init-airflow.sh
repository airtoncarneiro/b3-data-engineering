#!/bin/bash
set -e

export PATH="/opt/venv/bin:/workspaces/airflow/.local/bin:${PATH}"

echo "⚙️ Configurando variáveis do Airflow..." 

# Cria a variável B3_DOWNLOAD_ALL se não existir
if ! airflow variables get B3_DOWNLOAD_ALL >/dev/null 2>&1; then
    airflow variables set B3_DOWNLOAD_ALL "true" || { echo "Erro ao criar variável B3_DOWNLOAD_ALL"; exit 1; }
    echo "✅ Variável B3_DOWNLOAD_ALL criada com valor 'true'!"
else
    echo "👤 Variável B3_DOWNLOAD_ALL já existe!"
fi

echo "🔐 Airflow configurado com sucesso!"
echo "🔗 Acesse a interface web em: http://localhost:8080"
echo "👤 Usuário: $AIRFLOW_ADMIN_USER"
echo "🔑 Senha: $AIRFLOW_ADMIN_PASSWORD"
