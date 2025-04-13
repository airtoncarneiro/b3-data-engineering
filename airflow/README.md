# Projeto B3 Data Engineering - Ambiente Apache Airflow com Docker e DevContainer

Este projeto disponibiliza um ambiente de desenvolvimento completo e pronto para uso do **Apache Airflow**, utilizando **Docker** e **DevContainer**, ideal para atividades de engenharia de dados na **B3** (Bolsa de Valores Brasileira).

O ambiente foi configurado para facilitar o desenvolvimento local, incluindo scripts de inicialização, variáveis de ambiente parametrizadas e uma estrutura organizada para execução e testes de pipelines de dados (**DAGs**).

## 🚀 Tecnologias Utilizadas

| Tecnologia      | Versão    | Finalidade                  |
|----------------|-----------|----------------------------|
| Python         | 3.10      | Linguagem principal        |
| Apache Airflow | 2.10.5    | Orquestração de pipelines  |
| Docker         | Latest    | Containerização            |
| Docker Compose | Latest    | Orquestração dos containers|
| DevContainer   | VSCode Ext| Ambiente de desenvolvimento|

## 📂 Estrutura do Projeto

```text
.
├── dags/                   # Arquivos dos DAGs do Airflow
├── logs/                   # Logs gerados pelo Airflow
├── .env                    # Variáveis de ambiente (configurações sensíveis)
├── Dockerfile-Airflow      # Imagem customizada do Airflow
├── docker-compose-Airflow.yml # Orquestração dos containers
├── entrypoint.sh           # Script de entrypoint do container
├── init-airflow.sh         # Script de inicialização do Airflow
├── requirements.txt        # Dependências Python do projeto
├── .devcontainer/          # Configuração do DevContainer
└── .vscode/                # Configurações do VSCode
```

## 📋 Pré-requisitos

Para executar este projeto, você precisa ter instalado em sua máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Visual Studio Code](https://code.visualstudio.com/)
  - Extensão: *Dev Containers*
- [Git](https://git-scm.com/)

## ⚙️ Configuração do Ambiente Local

### 1. Clone o repositório

```bash
git clone [git@github.com:airtoncarneiro/b3-data-engineering.git](https://github.com/airtoncarneiro/b3-data-engineering)
cd b3-data-engineering
```

## 🔐 Configuração do arquivo .env

Este projeto utiliza variáveis de ambiente definidas no arquivo `.env`.

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Abra o arquivo .env e altere a variável AIRFLOW__CORE__FERNET_KEY com uma chave gerada pelo comando Python abaixo:

```python
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Altere também as variáveis AIRFLOW_ADMIN_USER e AIRFLOW_ADMIN_PASSWORD com o usuário e senha de sua escolha. 

### 2. Abra o projeto no VSCode

O VSCode detectará automaticamente o arquivo .devcontainer/devcontainer.json e sugerirá abrir o projeto dentro do DevContainer.

Caso isso não ocorra:

1. Abra o VSCode
2. Pressione `Ctrl+Shift+P`
3. Selecione: `Dev Containers: Reopen in Container`

### 3. Inicialização do Airflow

Após o devcontainer subir, o container executará automaticamente os scripts para inicializar o Airflow.

Acesse a interface web do Airflow:

- URL: http://localhost:8080
- Credenciais padrão:
  - Usuário: `admin`
  - Senha: `123456`

## 🧩 Configurações Importantes (.env)

| Variável | Descrição |
|----------|-----------|
| AIRFLOW_UID | UID do usuário local |
| AIRFLOW_ADMIN_USER / AIRFLOW_ADMIN_PASSWORD | Usuário e senha do admin |
| AIRFLOW__CORE__FERNET_KEY | Chave para criptografia |
| AIRFLOW__CORE__LOAD_EXAMPLES | Não carregar DAGs de exemplo |
| AIRFLOW__CORE__DAGS_FOLDER | Caminho das DAGs |
| AIRFLOW__LOGGING__BASE_LOG_FOLDER | Diretório dos logs |
| AIRFLOW__CORE__DEFAULT_TIMEZONE | Fuso horário |
| AIRFLOW__DEBUG__FAIL_FAST | Modo "fail fast" |

Para gerar uma nova FERNET_KEY:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 📦 Dependências Python

Principais pacotes no `requirements.txt`:

- apache-airflow[sqlite]==2.10.5
- httpx==0.27.0
- python-dateutil==2.8.2
- typing-extensions==4.10.0

> **Observação**: O SQLite é adequado para desenvolvimento. Em produção, considere PostgreSQL ou MySQL.

## ✨ Considerações Finais

Este ambiente é ideal para:

- Desenvolvimento de DAGs de engenharia de dados
- Estudos sobre Apache Airflow
- Execução local e testes isolados
- Ambiente seguro, parametrizado e replicável
