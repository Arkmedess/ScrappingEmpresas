# ScrappingEmpresas

Este projeto é uma ferramenta de automação desenvolvida em Python para enriquecimento de dados de empresas. A partir de um arquivo Excel contendo uma lista de CNPJs, o sistema consulta a **BrasilAPI** para obter informações detalhadas (como Razão Social, Endereço, Situação Cadastral, CNAE, etc.) e gera uma nova planilha com os dados consolidados.

## Pré-requisitos

Para executar este projeto, você precisará de:

- **Python 3.10+** (caso execute localmente)
- **Docker** (opcional, para execução em container)
- Um arquivo **.xlsx** contendo uma coluna obrigatória chamada `CNPJ`.

## Instalação

### Opção 1: Execução Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/ScrappingEmpresas.git
   cd ScrappingEmpresas
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Opção 2: Via Docker

1. **Construa a imagem:**
   ```bash
   docker build -t scrapping-empresas .
   ```

## Estrutura do Projeto

```
ScrappingEmpresas/
├── src/
│   ├── core/           # Lógica central de processamento e controle
│   ├── services/       # Integrações com APIs externas (BrasilAPI)
│   ├── utils/          # Utilitários (validadores, manipuladores de arquivos)
│   └── main.py         # Ponto de entrada da aplicação
├── docker-compose.yml  # Orquestração de containers (opcional)
├── Dockerfile          # Definição da imagem Docker
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

## Como Usar

### Executando Localmente

1. Tenha em mãos seu arquivo Excel (`.xlsx`) com a coluna `CNPJ`.
2. Execute o script principal:
   ```bash
   python src/main.py
   ```
3. Uma janela de seleção de arquivos será aberta. Escolha sua planilha de entrada.
4. O script processará linha por linha e exibirá o progresso no terminal.

### Executando via Docker

Para rodar com Docker e mapear um arquivo local para dentro do container:

```bash
docker run -v /caminho/para/seus/arquivos:/app/data scrapping-empresas python src/main.py /app/data/sua_planilha.xlsx
```

*(Nota: O diretório `/app/data` é apenas um ponto de montagem para que o container acesse seus arquivos locais. O `WORKDIR` interno do container é `/app`.)*

## Como Funciona

O sistema opera em um fluxo linear e robusto:

1.  **Leitura:** O arquivo Excel é carregado utilizando `pandas`.
2.  **Validação:** Cada CNPJ é higienizado (remoção de caracteres especiais) e validado (verificação de dígitos verificadores).
3.  **Consulta:** O sistema realiza chamadas à **BrasilAPI** para cada CNPJ válido.
4.  **Rate Limiting:** Um controlador interno gerencia as requisições para evitar bloqueios por excesso de chamadas (`429 Too Many Requests`).
5.  **Backup Automático:** A cada 35 registros processados, um arquivo temporário (`_TEMP.xlsx`) é salvo para evitar perda de dados em caso de falhas.
6.  **Finalização:** Ao concluir, um arquivo final (`_RESULTADO_FINAL.xlsx`) é gerado e o temporário é removido.

## Dados Retornados

O sistema enriquece a planilha original adicionando as seguintes colunas para cada CNPJ consultado:

- **Identificação:** `cnpj`, `razao_social`, `nome_fantasia`
- **Características:** `porte`, `descricao_porte`, `natureza_juridica`, `capital_social`
- **Atividade Econômica:** `CNAE` (Código), `DescricaoCNAE`
- **Endereço:** `TipoLogradouro`, `logradouro`, `numero`, `complemento`, `bairro`, `municipio`, `uf`, `cep`
- **Contato:** `telefone`, `telefone2`, `email`
- **Situação Cadastral:** `situacao_cadastral`, `descricao_motivo_situacao`, `data_situacao`
- **Status do Processamento:** `Status_Consulta` (indica se houve Sucesso, Erro, CNPJ Inválido, etc.)

## Funcionalidades

-   **Enriquecimento de Dados:** Busca automática de dados cadastrais completos.
-   **Validação de CNPJ:** Filtra e identifica CNPJs inválidos antes da consulta.
-   **Resiliência:** Tratamento de erros de rede e limites de API.
-   **Segurança de Dados:** Salvamento periódico (backup) durante o processamento.
-   **Flexibilidade:** Funciona via CLI ou com interface gráfica simples de seleção de arquivos.

## Stack Utilizada

-   **Python 3.10+**
-   **Pandas** (Manipulação de dados)
-   **Requests** (Requisições HTTP)
-   **OpenPyXL** (Leitura/Escrita de Excel)
-   **BrasilAPI** (Fonte de dados pública)
-   **Docker** (Containerização)

## Configurações e Limitações

-   **Coluna CNPJ:** É estritamente necessário que a planilha de entrada tenha uma coluna cabeçalho nomeada `CNPJ`.
-   **API Pública:** O projeto utiliza a BrasilAPI, que é um serviço público. O desempenho depende da disponibilidade e dos limites dessa API.

## Licença

Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar e modificar.

---
Desenvolvido como uma solução prática para automação de consultas cadastrais.
