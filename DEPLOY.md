# 🚀 Guia de Publicação - Criativa

Este documento explica como publicar a aplicação Criativa em uma plataforma online para ser acessada pela internet.

## ✅ Pré-requisitos

- ✓ Código já está no GitHub: `github.com/gr007-07/sistema-atelie-balao-magico`
- ✓ Arquivo `requirements.txt` pronto
- ✓ Aplicação testada localmente

## 📍 Opção 1: Render (RECOMENDADO - Mais Fácil)

### Passo 1: Acessar o Render
1. Acesse [https://render.com](https://render.com)
2. Clique em "Sign Up" e crie uma conta com sua conta GitHub
3. Autorize o acesso ao seu perfil GitHub

### Passo 2: Criar um novo Web Service
1. Clique em "New +" → "Web Service"
2. Selecione seu repositório `sistema-atelie-balao-magico`
3. Preencha os dados:
   - **Name**: criativa-app
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_atelie:app --host 0.0.0.0 --port 8000`

### Passo 3: Configurar variáveis (opcional)
Se precisar de variáveis de ambiente (como senha customizada):
1. Vá para "Environment"
2. Adicione as variáveis necessárias

### Passo 4: Deploy
1. Clique em "Create Web Service"
2. Aguarde o deploy (3-5 minutos)
3. Você recebe um link tipo: `https://criativa-app.onrender.com`

**Pronto! 🎉 Sua aplicação está online!**

---

## 📍 Opção 2: PythonAnywhere

### Passo 1: Criar conta
1. Acesse [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Clique em "Sign up" e escolha o plano gratuito
3. Confirme seu email

### Passo 2: Fazer upload do código
1. Na dashboard, clique em "Files"
2. Upload dos arquivos do projeto (ou use git clone)
3. Crie um virtual environment

### Passo 3: Configurar aplicação web
1. Vá para "Web" e clique em "Add a new web app"
2. Escolha "FastAPI"
3. Aponte para seu arquivo `api_atelie.py`
4. Recarregue a aplicação

**Você recebe um link tipo**: `seu-usuario.pythonanywhere.com`

---

## 📍 Opção 3: Railway

### Passo 1: Conectar GitHub
1. Acesse [https://railway.app](https://railway.app)
2. Clique "Start a New Project" → "Deploy from GitHub"
3. Selecione seu repositório

### Passo 2: Railway detecta automaticamente
A plataforma auto-configura baseado em `requirements.txt`

### Passo 3: Visualizar logs
1. Na aba "Deployments", acompanhe o processo
2. Você recebe um URL automático

---

## 🔐 Importante: Configurações para Produção

Antes de publicar, altere em `api_atelie.py`:

```python
# Linha 23 - Mude a senha padrão:
SENHA_OPERADOR = "sua-senha-segura-aqui"

# Linha 72 - Em produção, use HTTPS:
secure=True  # Mude de False para True
```

---

## 📝 Checklist Final

- [ ] `requirements.txt` está atualizado
- [ ] `.gitignore` está configurado
- [ ] Código foi feito push para GitHub
- [ ] Senha do operador foi alterada
- [ ] Banco de dados MySQL está configurado na produção
- [ ] URLs do banco de dados foram atualizadas em `conexao_banco.py`

---

## ❓ FAQ

**P: Qual plataforma escolho?**
R: Render é a mais fácil para iniciantes. PythonAnywhere também é ótima.

**P: O banco de dados funcionará?**
R: Se estiver usando localhost, precisará configurar um MySQL em nuvem (Clever Cloud, AWS RDS, etc).

**P: Como compartilho o link com os clientes?**
R: Simplesmente envie a URL fornecida pela plataforma (ex: `https://criativa-app.onrender.com`)

**P: Posso usar meu próprio domínio?**
R: Sim! Configure um domínio personalizado nas settings da plataforma.

---

## 🆘 Precisa de ajuda?

Se encontrar problemas no deployment, verifique:

### ❌ Erro: "syntax error near unexpected token"
Este erro acontece quando você usa código Python no Start Command:

```bash
# ❌ ERRADO (Python code):
uvicorn.run(app, host="127.0.0.1", port=8000)

# ✅ CERTO (Shell command):
uvicorn api_atelie:app --host 0.0.0.0 --port 8000
```

**Solução Render:**
1. Vá para Project Settings
2. Em "Start Command", altere para: `uvicorn api_atelie:app --host 0.0.0.0 --port 8000`
3. Clique "Save" e "Manual Deploy" → "Deploy latest commit"

### Outras verificações:
1. Logs da plataforma (eles mostram o erro)
2. Certifique-se que `api_atelie.py` está na raiz do repositório
3. Verifique se todas as dependências estão em `requirements.txt`
