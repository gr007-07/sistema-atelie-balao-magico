import unittest

from pedido_models import Cliente, Pedido


class PedidoTests(unittest.TestCase):
    def test_pedido_pode_anexar_fotos_exemplo(self):
        cliente = Cliente("Ana", "11999999999", "ana@email.com")
        pedido = Pedido(cliente, "2026-08-10", "2026-08-12")

        pedido.anexar_foto_exemplo("fotos/bolo.png")
        pedido.anexar_foto_exemplo("fotos/mesa.jpg")

        self.assertEqual(pedido.fotos_exemplo, ["fotos/bolo.png", "fotos/mesa.jpg"])

    def test_pedido_pode_definir_personalizacao(self):
        cliente = Cliente("Bruno", "11888888888", "bruno@email.com")
        pedido = Pedido(cliente, "2026-09-01", "2026-09-03")

        pedido.definir_personalizacao("Frozen", "rosa", "Maria", 5, "1kg")

        self.assertEqual(pedido.tema, "Frozen")
        self.assertEqual(pedido.cores, "rosa")
        self.assertEqual(pedido.nome_do_aniversariante, "Maria")


if __name__ == "__main__":
    unittest.main()
