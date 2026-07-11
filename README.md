# ✨ Sistema Criativa

Bem-vindo ao repositório da **Criativa - Loja dos Personalizados**! 
Este projeto foi desenvolvido para modernizar o gerenciamento de clientes e pedidos de artigos personalizados para festas.

O projeto é dividido em duas partes independentes para atender diferentes necessidades do negócio:

1. **Terminal Interno (CLI):** Um sistema rápido via terminal para uso no balcão da loja, focado no cadastro ágil de clientes e detalhamento de pedidos.
2. **API Web (FastAPI):** Uma interface moderna para uso local na máquina da loja.

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
pip install -r requirements.txt
```

### 3. Iniciando a aplicação Web
```bash
uvicorn api_atelie:app --host 127.0.0.1 --port 8010
```
Acesse em seu navegador: `http://127.0.0.1:8010`

### 4. Usando o sistema CLI (opcional)
```bash
python "script python.py"
```

## 📱 Usando a aplicação

### 👤 Para o Cliente
- Acesse a página inicial
- Preencha os dados do pedido
- Anexe fotos de referência (opcional)
- Clique em "Enviar Pedido"

### 👨‍💼 Para o Operador
- Acesse `/login` na aplicação web
- Digite a senha: `criativa123`
- Visualize todos os pedidos
- Atualize o status de cada pedido em tempo real

## 🔐 Segurança

- A página do operador está protegida por autenticação
- Senhas são validadas via sessão com cookie seguro (24 horas)
- Para alterar a senha, edite a variável `SENHA_OPERADOR` em `api_atelie.py`

## 📁 Estrutura do projeto

```
sistema-atelie-balao-magico/
├── api_atelie.py          # API principal (FastAPI)
├── conexao_banco.py       # Configuração de banco de dados
├── script python.py       # Interface CLI
├── pedido_models.py       # Modelos de dados
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
├── templates/             # Templates HTML
│   ├── index.html        # Página do cliente
│   ├── operador.html     # Painel do operador
│   └── login.html        # Página de login
├── static/               # Arquivos estáticos
│   └── styles.css        # Estilos da aplicação
├── uploads/              # Pasta para fotos anexadas
└── tests/                # Testes unitários
    └── test_pedido.py
```

## 📝 Notas
- O arquivo `requirements.txt` contém todas as dependências necessárias
- A aplicação deve ser executada somente na máquina local, usando `127.0.0.1`
- Não há configuração de link ou URL pública neste projeto
