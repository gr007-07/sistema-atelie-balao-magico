import os
import shutil
from pathlib import Path
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timedelta

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from conexao_banco import conectar_banco

app = FastAPI(title="API Criativa - Loja dos Personalizados")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Configuração de segurança simples
SENHA_OPERADOR = "criativa123"  # Altere em produção
SESSAO_TIMEOUT = 24  # Horas

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

pedidos_em_memoria: List[dict] = []
sessoes_ativas: dict = {}


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
    observacoes: str = ""


class AtualizacaoStatus(BaseModel):
    novo_status: str


@app.get("/", response_class=HTMLResponse)
async def pagina_cliente(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request, erro: Optional[str] = None):
    if request.cookies.get("operador_autenticado"):
        return RedirectResponse(url="/operador", status_code=302)
    return templates.TemplateResponse(request, "login.html")


@app.post("/api/login")
async def login_operador(senha: str = Form(...)):
    if senha != SENHA_OPERADOR:
        return RedirectResponse(url="/login?erro=1", status_code=302)
    
    response = RedirectResponse(url="/operador", status_code=302)
    response.set_cookie(
        "operador_autenticado",
        value="true",
        max_age=SESSAO_TIMEOUT * 3600,
        httponly=True,
        secure=False  # Mude para True em produção (HTTPS)
    )
    return response


@app.get("/operador", response_class=HTMLResponse)
async def pagina_operador(request: Request):
    if not request.cookies.get("operador_autenticado"):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(request, "operador.html")


@app.get("/logout")
async def logout_operador():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("operador_autenticado")
    return response


@app.post("/api/novo-pedido")
async def receber_pedido_do_site(
    nome_cliente: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    data_festa: str = Form(...),
    data_entrega: str = Form(...),
    tema: str = Form(...),
    cores: str = Form(...),
    nome_aniv: str = Form(...),
    idade: int = Form(...),
    tamanho_bolo: float = Form(...),
    observacoes: str = Form(default=""),
    arquivos: List[UploadFile] = File(default=[]),
):
    fotos_salvas: List[str] = []

    for upload in arquivos or []:
        if not upload.filename:
            continue
        extensao = Path(upload.filename).suffix.lower() or ".jpg"
        nome_arquivo = f"{uuid4().hex}{extensao}"
        caminho = UPLOAD_DIR / nome_arquivo
        with caminho.open("wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        fotos_salvas.append(f"/uploads/{nome_arquivo}")

    dados = DadosDoSite(
        nome_cliente=nome_cliente,
        telefone=telefone,
        email=email,
        data_festa=data_festa,
        data_entrega=data_entrega,
        tema=tema,
        cores=cores,
        nome_aniv=nome_aniv,
        idade=idade,
        tamanho_bolo=tamanho_bolo,
        observacoes=observacoes,
    )

    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql_cliente = "INSERT INTO CLIENTES (NOME, EMAIL) VALUES (%s, %s)"
            cursor.execute(sql_cliente, (dados.nome_cliente, dados.email))
            id_cliente = cursor.lastrowid

            sql_telefone = "INSERT INTO TELEFONE (TIPO, NUMERO, ID_CLIENTE) VALUES (%s, %s, %s)"
            cursor.execute(sql_telefone, ("CEL", dados.telefone, id_cliente))

            sql_pedido = """INSERT INTO PEDIDOS
                            (DATA_FESTA, DATA_ENTREGA, STATUS, TEMA, CORES, NOME_ANIV, IDADE, TAMANHO_BOLO, ID_CLIENTE)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores_pedido = (
                dados.data_festa,
                dados.data_entrega,
                "Orçamento",
                dados.tema,
                dados.cores,
                dados.nome_aniv,
                dados.idade,
                dados.tamanho_bolo,
                id_cliente,
            )
            cursor.execute(sql_pedido, valores_pedido)
            id_pedido = cursor.lastrowid
            conexao.commit()

            return {
                "sucesso": True,
                "mensagem": f"Pedido #{id_pedido} criado com sucesso!",
                "id_pedido": id_pedido,
                "fotos_exemplo": fotos_salvas,
            }
        except Exception as e:  # pragma: no cover - fallback genérico para o ambiente local
            conexao.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao salvar: {str(e)}") from e
        finally:
            cursor.close()
            conexao.close()

    novo_pedido = {
        "id_pedido": len(pedidos_em_memoria) + 1,
        "cliente_nome": dados.nome_cliente,
        "telefone": dados.telefone,
        "email": dados.email,
        "data_festa": dados.data_festa,
        "data_entrega": dados.data_entrega,
        "status": "Orçamento",
        "tema": dados.tema,
        "cores": dados.cores,
        "nome_aniv": dados.nome_aniv,
        "idade": dados.idade,
        "tamanho_bolo": dados.tamanho_bolo,
        "observacoes": dados.observacoes,
        "fotos_exemplo": fotos_salvas,
    }
    pedidos_em_memoria.append(novo_pedido)
    return {
        "sucesso": True,
        "mensagem": f"Pedido #{novo_pedido['id_pedido']} criado com sucesso (modo demonstração)!",
        "id_pedido": novo_pedido["id_pedido"],
        "fotos_exemplo": fotos_salvas,
    }


@app.get("/api/pedidos")
def listar_todos_os_pedidos():
    conexao = conectar_banco()
    if conexao:
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
                lista_de_pedidos.append(
                    {
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
                        "tamanho_bolo": float(linha[11]),
                        "observacoes": "",
                        "fotos_exemplo": [],
                    }
                )

            return {"total_pedidos": len(lista_de_pedidos), "pedidos": lista_de_pedidos}
        except Exception as e:  # pragma: no cover - fallback genérico para o ambiente local
            raise HTTPException(status_code=400, detail=f"Erro ao buscar histórico: {str(e)}") from e
        finally:
            cursor.close()
            conexao.close()

    return {"total_pedidos": len(pedidos_em_memoria), "pedidos": pedidos_em_memoria}


@app.put("/api/pedidos/{id_pedido}/status")
def atualizar_status_pedido(id_pedido: int, dados: AtualizacaoStatus):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql_update = "UPDATE PEDIDOS SET STATUS = %s WHERE ID_PEDIDOS = %s"
            cursor.execute(sql_update, (dados.novo_status, id_pedido))
            conexao.commit()

            if cursor.rowcount > 0:
                return {"sucesso": True, "mensagem": f"Pedido #{id_pedido} atualizado para: '{dados.novo_status}'."}
            raise HTTPException(status_code=404, detail=f"Nenhum pedido encontrado com o ID {id_pedido}.")
        except Exception as e:  # pragma: no cover - fallback genérico para o ambiente local
            conexao.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}") from e
        finally:
            cursor.close()
            conexao.close()

    for pedido in pedidos_em_memoria:
        if pedido["id_pedido"] == id_pedido:
            pedido["status"] = dados.novo_status
            return {"sucesso": True, "mensagem": f"Pedido #{id_pedido} atualizado para: '{dados.novo_status}'."}

    raise HTTPException(status_code=404, detail=f"Nenhum pedido encontrado com o ID {id_pedido}.")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)