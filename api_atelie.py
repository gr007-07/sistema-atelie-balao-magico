from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

# 1. INICIALIZA A API
app = FastAPI(title="API Ateliê Balão Mágico")

# 2. MOLDE DOS DADOS (O que o site envia)
class DadosDoSite(BaseModel):
    nome_cliente: str
    telefone: str
    email: str
    data_festa: str
    data_entrega: str
    tema: str
    cores: str
    nome_aniv: str
    idade: int
    tamanho_bolo: float

# 3. FUNÇÃO DE CONEXÃO AO BANCO
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='ATELIE',
            user='root',
            password='12345678' 
        )
        return conexao
    except Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None

# ==========================================
# ROTA 1: CRIAR UM NOVO PEDIDO (POST)
# ==========================================
@app.post("/api/novo-pedido")
def receber_pedido_do_site(dados: DadosDoSite):
    conexao = conectar_banco()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro de conexão com o BD.")
    
    cursor = conexao.cursor()
    try:
        sql_cliente = "INSERT INTO CLIENTES (NOME, EMAIL) VALUES (%s, %s)"
        cursor.execute(sql_cliente, (dados.nome_cliente, dados.email))
        id_cliente = cursor.lastrowid
        
        sql_telefone = "INSERT INTO TELEFONE (TIPO, NUMERO, ID_CLIENTE) VALUES (%s, %s, %s)"
        cursor.execute(sql_telefone, ('CEL', dados.telefone, id_cliente))
        
        sql_pedido = """INSERT INTO PEDIDOS 
                        (DATA_FESTA, DATA_ENTREGA, STATUS, TEMA, CORES, NOME_ANIV, IDADE, TAMANHO_BOLO, ID_CLIENTE) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores_pedido = (dados.data_festa, dados.data_entrega, 'Orçamento', 
                          dados.tema, dados.cores, dados.nome_aniv, dados.idade, dados.tamanho_bolo, id_cliente)
        
        cursor.execute(sql_pedido, valores_pedido)
        id_pedido = cursor.lastrowid
        conexao.commit()
        
        return {
            "sucesso": True, 
            "mensagem": f"Pedido #{id_pedido} para {dados.nome_cliente} criado com sucesso!"
        }
    except Error as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao salvar: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# ==========================================
# ROTA 2: BUSCAR TODOS OS PEDIDOS (GET)
# ==========================================
@app.get("/api/pedidos")
def listar_todos_os_pedidos():
    conexao = conectar_banco()
# Crie este "molde" para o status logo abaixo da classe DadosDoSite, ou aqui mesmo:
class AtualizacaoStatus(BaseModel):
    novo_status: str

# ==========================================
# ROTA 3: ATUALIZAR STATUS DO PEDIDO (PUT)
# ==========================================
@app.put("/api/pedidos/{id_pedido}/status")
def atualizar_status_pedido(id_pedido: int, dados: AtualizacaoStatus):
    """
    Esta rota recebe o ID do pedido pela URL e o novo status pelo texto (JSON),
    e faz o UPDATE direto no MySQL.
    """
    conexao = conectar_banco()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro de conexão com o Banco de Dados.")
    
    cursor = conexao.cursor()
    try:
        sql_update = "UPDATE PEDIDOS SET STATUS = %s WHERE ID_PEDIDOS = %s"
        cursor.execute(sql_update, (dados.novo_status, id_pedido))
        conexao.commit()
        
        # Verifica se o pedido realmente existia no banco
        if cursor.rowcount > 0:
            return {"sucesso": True, "mensagem": f"O Pedido #{id_pedido} foi atualizado para: '{dados.novo_status}'."}
        else:
            raise HTTPException(status_code=404, detail=f"Nenhum pedido encontrado com o ID {id_pedido}.")
            
    except Error as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cursor.close()
        conexao.close()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro de conexão com o Banco de Dados.")
    
    cursor = conexao.cursor()
    try:
        sql_busca = """SELECT P.ID_PEDIDOS, C.NOME, T.NUMERO, C.EMAIL, 
                              P.DATA_FESTA, P.DATA_ENTREGA, P.STATUS, 
                              P.TEMA, P.CORES, P.NOME_ANIV, P.IDADE, P.TAMANHO_BOLO 
                       FROM PEDIDOS P 
                       INNER JOIN CLIENTES C ON C.IDCLIENTE = P.ID_CLIENTE
                       LEFT JOIN TELEFONE T ON C.IDCLIENTE = T.ID_CLIENTE"""
                       
        cursor.execute(sql_busca)
        resultados = cursor.fetchall()
        
        lista_de_pedidos = []
        for linha in resultados:
            pedido = {
                "id_pedido": linha[0],
                "cliente_nome": linha[1],
                "telefone": linha[2],
                "email": linha[3],
                "data_festa": str(linha[4]), 
                "data_entrega": str(linha[5]),
                "status": linha[6],
                "tema": linha[7],
                "cores": linha[8],
                "nome_aniv": linha[9],
                "idade": linha[10],
                "tamanho_bolo": float(linha[11]) 
            }
            lista_de_pedidos.append(pedido)
            
        return {"total_pedidos": len(lista_de_pedidos), "pedidos": lista_de_pedidos}
        
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar histórico: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# ==========================================
# INICIAR O SERVIDOR (O TRUQUE DO PLAY)
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)