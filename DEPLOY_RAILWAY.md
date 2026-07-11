# 🚀 Guia de Deploy no Railway

## Passo 1: Preparar o Repositório
✅ Já feito! Os arquivos necessários foram criados:
- `Procfile` - Configuração de como rodar
- `.env.example` - Exemplo de variáveis de ambiente
- `conexao_banco.py` - Atualizado para usar variáveis de ambiente

## Passo 2: Criar conta no Railway
1. Acesse: https://railway.app
2. Faça login com GitHub
3. Crie um novo projeto

## Passo 3: Conectar seu repositório GitHub
1. No Railway, clique em "New Project"
2. Selecione "Deploy from GitHub"
3. Autorize e selecione o repositório `sistema-atelie-balao-magico`

## Passo 4: Configurar variáveis de ambiente
No Railway, vá para "Variables" e adicione:
```
DB_HOST=seu_mysql_host
DB_PORT=3306
DB_NAME=ATELIE
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
HOST=0.0.0.0
PORT=8000
```

⚠️ **Importante**: Se o MySQL está em uma máquina local, você precisa:
- Ativar acesso remoto no MySQL, OU
- Usar um MySQL em cloud (PlanetScale, AWS RDS, etc.)

## Passo 5: Deploy automático
- Railway faz deploy automaticamente a cada push no GitHub
- Você pode acompanhar em "Deployments"

## Resultado
Sua aplicação estará em uma URL pública como:
```
https://seu-projeto-production.up.railway.app
```

## Troubleshooting
- Ver logs: `railway logs`
- Deploy manual: `railway deploy`
- Mais info: https://docs.railway.app

---

### Alternativa: MySQL em Cloud
Para facilitar, recomendo usar:
- **PlanetScale** (MySQL grátis) - https://planetscale.com
- **Render** - https://render.com (MySQL e Railway em um lugar)
