#!/bin/bash
set -e

# export PATH="/opt/venv/bin:/workspaces/airflow/.local/bin:${PATH}"

echo "⚙️ Configurando variáveis do Airflow..." 

# Cria a variável B3_CONFIG_DOWNLOAD_SERIE se não existir.
## Esta variável é usada para armazenar o tipo de série a ser baixada
## no Airflow. O valor padrão é "series_anuais", que representa as séries anuais.
## Depois do primeiro processamento, esta variável assume o valor "serie_diaria"
## que representa as séries diárias.
if ! airflow variables get B3_CONFIG_DOWNLOAD_SERIE >/dev/null 2>&1; then
    airflow variables set B3_CONFIG_DOWNLOAD_SERIE "series_anuais" || { echo "Erro ao criar variável B3_CONFIG_DOWNLOAD_SERIE"; exit 1; }
    echo "✅ Variável B3_CONFIG_DOWNLOAD_SERIE criada com valor 'series_anuais'!"
else
    echo "👤 Variável B3_CONFIG_DOWNLOAD_SERIE já existe!"
fi


# Cria a variável B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE se não existir.
## Esta variável determina desde que ano deve ser feito o download
## das séries anuais.
## A série anual começou em 1996.
if ! airflow variables get B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE >/dev/null 2>&1; then
    airflow variables set B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE "2023" || { echo "Erro ao criar variável B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE"; exit 1; }
    echo "✅ Variável B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE criada com valor 'series_anuais'!"
else
    echo "👤 Variável B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE já existe!"
fi

echo "🔐 Airflow configurado com sucesso!"
echo "🔗 Acesse a interface web em: http://localhost:8080"
echo "👤 Usuário: $AIRFLOW_ADMIN_USER"
echo "🔑 Senha: $AIRFLOW_ADMIN_PASSWORD"
