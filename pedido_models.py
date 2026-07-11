from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Cliente:
    nome: str
    telefone: str
    email: str
    historico_de_compras: List[str] = field(default_factory=list)
    datas_de_aniversarios: List[str] = field(default_factory=list)


@dataclass
class Pedido:
    cliente: Cliente
    data_festa: str
    data_entrega: str
    status: str = "Orçamento"
    tema: str = ""
    cores: str = ""
    nome_do_aniversariante: str = ""
    idade: Optional[int] = None
    tamanho_do_bolo: str = ""
    fotos_exemplo: List[str] = field(default_factory=list)
    observacoes: str = ""

    def anexar_foto_exemplo(self, caminho: str) -> None:
        if caminho.strip():
            self.fotos_exemplo.append(caminho.strip())

    def definir_personalizacao(self, tema: str, cores: str, nome: str, idade: int, tamanho: str) -> None:
        self.tema = tema
        self.cores = cores
        self.nome_do_aniversariante = nome
        self.idade = idade
        self.tamanho_do_bolo = tamanho

    def exibir_info(self) -> None:
        print("\n--- Resumo do Pedido ---")
        print(f"Cliente: {self.cliente.nome} | telefone: {self.cliente.telefone} | email: {self.cliente.email}")
        print(f"Tema: {self.tema}")
        print(f"Cores: {self.cores}")
        print(f"Nome do Aniversariante: {self.nome_do_aniversariante}")
        print(f"Idade: {self.idade}")
        print(f"Tamanho do bolo: {self.tamanho_do_bolo}")
        if self.fotos_exemplo:
            print(f"Fotos anexadas: {', '.join(self.fotos_exemplo)}")
        print(f"Status atual: {self.status}")
        print("------------------------\n")
