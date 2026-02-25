# 🎈 Sistema Ateliê Balão Mágico

Bem-vindo ao repositório do **Ateliê Balão Mágico**! 
Este projeto foi desenvolvido para modernizar o gerenciamento de clientes e pedidos de artigos personalizados para festas.

O projeto é dividido em duas partes independentes para atender diferentes necessidades do negócio:

1. **Terminal Interno (CLI):** Um sistema rápido via terminal para uso no balcão da loja, focado no cadastro ágil de clientes e detalhamento de pedidos.
2. **API Web (FastAPI):** Uma interface moderna e documentada, pronta para ser conectada ao site oficial do ateliê ou a um aplicativo de clientes.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Framework Web:** FastAPI & Uvicorn
* **Banco de Dados:** MySQL
* **Integração:** `mysql-connector-python`

## 🚀 Como rodar o projeto na sua máquina

### 1. Preparando o Banco de Dados
Certifique-se de ter o MySQL (ou pacotes como XAMPP/WAMP) rodando. Crie um banco de dados chamado `ATELIE` e configure as tabelas `CLIENTES`, `TELEFONE` e `PEDIDOS`.

### 2. Instalando as dependências
Abra o terminal na pasta do projeto e instale as bibliotecas necessárias:
```bash
pip install fastapi uvicorn mysql-connector-python pydantic
