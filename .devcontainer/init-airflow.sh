#!/bin/bash
set -e

export PATH="/home/airflow/.local/bin:${PATH}"

echo "🔧 Inicializando Airflow com usuário admin/admin..."

# Inicializa banco de dados
airflow db migrate

# Verifica se o usuário já existe
if ! airflow users list | grep -q "admin"; then
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname Dev \
        --role Admin \
        --email admin@example.com \
        --password admin
    echo "✅ Usuário admin criado com sucesso!"
else
    echo "👤 Usuário admin já existe!"
fi

# Cria a variável B3_DOWNLOAD_ALL se ela não existir
if ! airflow variables get B3_DOWNLOAD_ALL >/dev/null 2>&1; then
    airflow variables set B3_DOWNLOAD_ALL "true"
    echo "✅ Variável B3_DOWNLOAD_ALL criada com valor 'true'!"
else
    echo "👤 Variável B3_DOWNLOAD_ALL já existe!"
fi

echo -e "✅ Configuração concluída.\nLogue na UI com usuário e senha 'admin'."
