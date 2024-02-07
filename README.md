# B3 Data Engineering

Projeto de Engenharia de Dados (ED) que terá como fonte primária os dados da Bolsa de Valores do Brasil visando a aprendizagem, a fixação e o repasse de conhecimentos para outros interessados na área.
Sua implementação será gradual e dividada em etapas para melhor entendimento de quem está aprendendo. Assim, serão criados *branchs* para cada etapa distinta de desenvolvimento e, cada uma delas, serão *"mergeadas"* na *main* à medida que avançarmos.

# Índice

- Introdução
	- [Sobre mim](#sobre-mim)
	- [Objetivos do projeto](#objetivos-do-projeto)
	- [Sobre a modularização do projeto em *branchs*](#sobre-as-branchs)
	- [Descrição do Projeto](#descrição-do-projeto)

## Sobre Mim

Como aqui não tenho interesse em falar muito sobre mim (vide [LinkedIn][1]), falarei apenas que: já trabalho na área de TI desde 1992 como desenvolvedor de software e em 2019 me despertou o interesse pelo *Big Data*. Fiz alguns cursos, li muito e em Fev/22 tive a primeira oportunidade de trabalhar exclusivamente como ED.

## Objetivos do Projeto

Tendo como interesse desenvolver um projeto que abranja o máximo de **hard skills* possíveis para aprendizado, fixação de conhecimentos e - por quê não? - demonstrar aos recrutadores as habilidades adquiridas, buscarei interagir com:
- [ ] **Docker** para desenvolvimento local
- [ ] **Minikube** para orquestração de containers
- [ ] **Airflow** para orquestração de pipeline
- [ ] **Apache Spark** para processamento de dados
- [ ] **Terraform** para IaC
- [ ] **Armazenamento de Objetos** para armazenamento usando Minio (talvez evoluindo para S3)
 - e outros, tais como: Data Catalog, Trino, DataFlow, CDC, ArgoCD, Dagster, CI/CD, AWS.

Obs 1: Talvez nem todas as stacks possam ser usadas em conjunto ou, ainda, nem este projeto as suporta. Mas deixo registrado como interesse e, quem sabe, criar um novo projeto que suporte aquelas que não foram utilizadas aqui.
Obs 2: A ideia é deixar o projeto totalmente reproduzível para aqueles que queiram estudar e/ou melhorá-lo.

## Sobre a modularização do projeto em *branchs*

Haverá a branch principal (*main*) que contemplará o projeto como um todo. Todas as demais *branchs* estarão no escopo da stack de aplicação do projeto. Com isto, busco criar uma leitura do tipo passo a passo e, assim, facilitar o entendimento de quem quer aprender. Em cada branch estarão sendo explicados os passos, as configurações e o desenvolvimento para que a referida etapa aconteça.

# Descrição do Projeto
A [B3][2] é a Bolsa de Valores do Brasil e passei a ter interesse em investimentos em 2022. Quem investe em ações da B3 está investindo em Rendas Variáveis e todo investidor fica sempre de olho no valor da ação e seus possíveis dividendos.
A B3 disponibiliza para download sempre ao final do dia o [histórico das cotações][3] das ações. Podem ser realizados o download das ações:

 - Por ano: onde se escolhe o ano
 - Dos últimos 12 meses: onde se escolhe o mês
 - Por data (do ano corrente): onde se escolhe o mês e dia

O arquivo virá no formato ZIP e contém um ou mais arquivos TXT com os dados das ações:

 - nome da empresa
 - código da empresa
 - código da ação
 - código ISIN
 - tipo de mercado (a vista, termo, opções)
 - especificação (ON/PN)
 - preços (anterior, abertura, mínimo, médio, máximo, fechamento)
 - quantidade de negócios e volume negociado com o papel
 - dentre outros dados disponíveis.

O projeto consistirá em realizar o download do histórico, processá-lo e disponibilizar os dados num DW para uma visualização no dashboard.

[1]: https://www.linkedin.com/in/airton-carneiro
[2]: https://www.b3.com.br
[3]: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/

