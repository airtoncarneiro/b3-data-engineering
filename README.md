# Engenharia de Dados B3

Projeto de engenharia de dados que extrai, processa e analisa dados históricos de ações da B3 (Bolsa de Valores do Brasil).

## Visão Geral

Este projeto visa criar um pipeline automatizado para:
1. Download de dados históricos de ações da B3
2. Processamento e transformação dos dados
3. Armazenamento em um data warehouse
4. Visualização dos resultados em um dashboard

Os dados incluem informações da empresa, códigos de ações, tipos de mercado, preços (anterior, abertura, mínimo, máximo, fechamento), volume de negociações e mais.

## Tecnologias Utilizadas

- **Docker** - Ambiente de desenvolvimento containerizado
- **Apache Airflow** - Orquestração de workflows
- **Python** - Processamento de dados
- Implementações futuras planejadas:
  - Minikube para orquestração de containers
  - Apache Spark para processamento de dados em larga escala
  - Terraform para infraestrutura como código
  - MinIO/S3 para armazenamento de objetos
  - Ferramentas de visualização de dados

## Estrutura do Projeto

```
.
├── .devcontainer/         # Configuração do container de desenvolvimento
│   ├── Dockerfile
│   ├── devcontainer.json
│   ├── init-airflow.sh
│   └── requirements.txt
├── airflow/              # Configuração do Airflow e DAGs
│   ├── dags/
│   └── airflow.cfg
├── .vscode/             # Configurações do VS Code
└── README.md
```

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [VS Code](https://code.visualstudio.com/)
- [Extensão Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Como Começar

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/b3-data-engineering.git
cd b3-data-engineering
```

2. Abra o projeto no VS Code:
```bash
code .
```

3. Quando solicitado, clique em "Reabrir no Container" ou pressione F1 e selecione "Dev Containers: Reabrir no Container"

4. Aguarde o container ser construído e inicializado. O script de inicialização irá:
   - Configurar o banco de dados do Airflow
   - Criar usuário administrador (usuário: admin, senha: admin)
   - Iniciar o webserver e scheduler do Airflow

5. Acesse a interface do Airflow:
   - Abra http://localhost:8080 no navegador
   - Faça login com usuário: admin, senha: admin

## Desenvolvimento

O ambiente de desenvolvimento inclui:
- Python 3.10 com ambiente virtual
- Apache Airflow 2.10.5
- Extensões do VS Code para desenvolvimento Python
- Webserver e scheduler do Airflow rodando em sessões tmux

### Adicionando Novas DAGs

1. Crie seus arquivos DAG em `airflow/dags`
2. As DAGs serão automaticamente detectadas pelo Airflow
3. Visualize e acione-as pela interface do Airflow

### Status do Projeto

Este é um trabalho em andamento. Implementação atual:
- [x] Configuração do ambiente de desenvolvimento com Docker
- [x] Configuração básica do Airflow
- [ ] Extração de dados da B3
- [ ] Pipeline de processamento de dados
- [ ] Configuração do data warehouse
- [ ] Visualização em dashboard

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

## Licença

Este projeto está licenciado sob a Apache License 2.0 - consulte o arquivo `LICENSE` para detalhes.

## Autor

[Airton Carneiro](https://www.linkedin.com/in/airton-carneiro) - Engenheiro de Dados com mais de 30 anos de experiência em TI.

## Fonte dos Dados

Os dados históricos das ações são obtidos através do [Histórico B3](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/).

## Branchs do Projeto

O desenvolvimento é realizado em branches separadas para facilitar o aprendizado:
- `main`: Versão estável e completa do projeto completo
- `airflow-dev`: Implementação do Apache Airflow

[1]: https://www.linkedin.com/in/airton-carneiro
[2]: https://www.b3.com.br
[3]: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/

