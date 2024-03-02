
# B3 Data Engineering (Airflow-Dev)

  

Nesta parte do projeto vamos configurar nosso ambiente de desenvolvimento do Airflow e desenvolver nossa DAG. Faremos tudo localmente para testes e depois evoluiremos.

## Configurando o ambiente
Requisitos:
 - Criar um ambiente virtual de desenvolvimento
 - Instalar o Airflow (pip)
 - Criar as variáveis de ambiente
 - Testar o ambiente

### Criando o ambiente virtual
Usar um programa de sua escolha (conda, pyenv, venv, etc). Neste exemplo usaremos o conda. Acesse o terminal e siga os procedimentos abaixo.

    > conda create -n b3 python=3.10
    > conda activate b3
    > pip install "apache-airflow[celery]==2.8.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.2/constraints-3.10.txt"
    > airflow version

Após isso, crie a variável de ambiente `AIRFLOW_HOME` apontando para a pasta `AIRFLOW`.
Entre na pasta `AIRFLOW`.

    > export AIRFLOW_HOME=$(PWD)

obs: adeque o comando acima ao seu sistema operacional. No meu caso, estou usando o aplicativo `direnv` (instalado pelo PIP) que automaticamente carrega para as variáveis de ambiente o que está no arquivo `.envrc`.

Agora vamos executar o Airflow em modo *Standalone*.

    > airflow standalone

Você verá um monte de mensagens surgindo no terminal e, se tudo estiver OK, ele exibirá a mensagem de que o Airflow está rodando e informando para acessar a URL indicada.
Para realizar o login, usar `admin` como usuário e usar a senha informada no terminal.