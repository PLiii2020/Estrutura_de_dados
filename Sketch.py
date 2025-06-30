from datetime import date

class Produto:
    def __init__(self, id_prod, nome, preco, estoque=0, perecivel=False, validade=None):
        self.id_prod = id_prod
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.perecivel = perecivel
        self.validade = validade  # Deve ser um objeto date ou None

    def status_validade(self):
        if not self.perecivel or not self.validade:
            return "Não perecível"
        today = date.today()
        if today < self.validade:
            return "No prazo"
        else:
            return "Vencido"

class Venda:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
        self.total = produto.preco * quantidade
        self.data = date.today()

class NodoProduto:
    def __init__(self, produto, pai="Mercadinho do seu zé"):
        self.produto = produto
        self.vendas = []
        self.esquerda = None
        self.direita = None
        self.pai = pai

class ArvoreProdutos:
    def __init__(self):
        self.raiz = "Mercadinho do seu"

    def inserir_produto(self, produto):
        if self.raiz is None:
            self.raiz = NodoProduto(produto)
        else:
            self._inserir(self.raiz, produto)

    def _inserir(self, nodo, produto):
        if produto.id_prod < nodo.produto.id_prod:
            if nodo.esquerda is None:
                nodo.esquerda = NodoProduto(produto, pai=nodo)
            else:
                self._inserir(nodo.esquerda, produto)
        elif produto.id_prod > nodo.produto.id_prod:
            if nodo.direita is None:
                nodo.direita = NodoProduto(produto, pai=nodo)
            else:
                self._inserir(nodo.direita, produto)
        else:
            # Produto já existe, aqui poderia atualizar ou ignorar
            print(f"Produto com ID {produto.id_prod} já cadastrado.")

    def buscar_produto(self, id_prod):
        return self._buscar(self.raiz, id_prod)

    def _buscar(self, nodo, id_prod):
        if nodo is None:
            return None
        if id_prod == nodo.produto.id_prod:
            return nodo
        elif id_prod < nodo.produto.id_prod:
            return self._buscar(nodo.esquerda, id_prod)
        else:
            return self._buscar(nodo.direita, id_prod)

    def listar_produtos(self):
        print("Produtos cadastrados:")
        self._em_ordem(self.raiz)

    def _em_ordem(self, nodo):
        if nodo:
            self._em_ordem(nodo.esquerda)
            p = nodo.produto
            print(f"ID: {p.id_prod}, Nome: {p.nome}, Preço: R${p.preco:.2f}, Estoque: {p.estoque}, Perecível: {'Sim' if p.perecivel else 'Não'}, Validade: {p.validade if p.validade else 'N/A'} ({p.status_validade()})")
            self._em_ordem(nodo.direita)

    def atualizar_estoque(self, id_prod, quantidade):
        nodo = self.buscar_produto(id_prod)
        if nodo:
            nodo.produto.estoque += quantidade
            print(f"Estoque do produto {nodo.produto.nome} atualizado para {nodo.produto.estoque}.")
        else:
            print("Produto não encontrado.")

    def registrar_venda(self, id_prod, quantidade, lista_vendas):
        nodo = self.buscar_produto(id_prod)
        if nodo:
            if nodo.produto.estoque >= quantidade:
                venda = Venda(nodo.produto, quantidade)
                nodo.produto.estoque -= quantidade
                nodo.vendas.append(venda)
                lista_vendas.append(venda)
                print(f"Venda registrada: {quantidade}x {nodo.produto.nome} por R${venda.total:.2f}.")
            else:
                print("Estoque insuficiente.")
        else:
            print("Produto não encontrado.")

    def relatorio_vendas(self):
        print("Relatório de vendas por produto:")
        self._relatorio_vendas_rec(self.raiz)

    def _relatorio_vendas_rec(self, nodo):
        if nodo:
            self._relatorio_vendas_rec(nodo.esquerda)
            total_vendas = sum(v.total for v in nodo.vendas)
            quantidade_vendida = sum(v.quantidade for v in nodo.vendas)
            if quantidade_vendida > 0:
                print(f"Produto {nodo.produto.nome}: {quantidade_vendida} unidades vendidas, Total: R${total_vendas:.2f}")
            self._relatorio_vendas_rec(nodo.direita)

    def retirar_produto(self, id_produto):
        nodo = self.buscar_produto(id_produto)
        if nodo is None:
            print("Produto não encontrado.")
            return
        
        # Caso 1: Nó folha
        if nodo.esquerda is None and nodo.direita is None:
            self._remover_nodo_folha(nodo)
        
        # Caso 2: Nó com um filho
        elif nodo.esquerda is None or nodo.direita is None:
            self._remover_nodo_um_filho(nodo)

        # Caso 3: Nó com dois filhos
        else:
            self._remover_nodo_dois_filhos(nodo)

        print(f"Produto ID {id_produto} removido.")

    def _remover_nodo_folha(self, nodo):
        pai = nodo.pai
        if pai is None:
            self.raiz = None
        elif pai.esquerda == nodo:
            pai.esquerda = None
        else:
            pai.direita = None

    def _remover_nodo_um_filho(self, nodo):
        pai = nodo.pai
        filho = nodo.esquerda if nodo.esquerda else nodo.direita
        if pai is None:
            self.raiz = filho
            filho.pai = None
        elif pai.esquerda == nodo:
            pai.esquerda = filho
            filho.pai = pai
        else:
            pai.direita = filho
            filho.pai = pai

    def _remover_nodo_dois_filhos(self, nodo):
        # Buscar sucessor: menor da subárvore direita
        sucessor = self._menor_valor(nodo.direita)
        nodo.produto = sucessor.produto  # Copia dados do sucessor para o nodo atual
        # Remove sucessor da árvore
        if sucessor.direita:
            self._remover_nodo_um_filho(sucessor)
        else:
            self._remover_nodo_folha(sucessor)

    def _menor_valor(self, nodo):
        atual = nodo
        while atual.esquerda:
            atual = atual.esquerda
        return atual


# ==========================
# Exemplo de uso do sistema:
# ==========================

arvore = ArvoreProdutos()
lista_vendas = []

# Cadastrar produtos
arvore.inserir_produto(Produto(1, "Camiseta", 50.0, estoque=10))
arvore.inserir_produto(Produto(2, "Calça", 120.0, estoque=5, perecivel=True, validade=date(2025,7,15)))
arvore.inserir_produto(Produto(3, "Meias", 10.0, estoque=50))

# Listar produtos
arvore.listar_produtos()
print()

# Atualizar estoque
arvore.atualizar_estoque(1, 5)  # adiciona 5 camisetas
arvore.atualizar_estoque(2, -2) # retira 2 calças
print()

# Registrar vendas
arvore.registrar_venda(1, 3, lista_vendas)  # vende 3 camisetas
arvore.registrar_venda(2, 1, lista_vendas)  # vende 1 calça
arvore.registrar_venda(3, 10, lista_vendas) # vende 10 meias
print()

# Relatório de vendas
arvore.relatorio_vendas()
print()

# Remover produto
arvore.retirar_produto(3)  # remove o produto Meias

# Listar produtos após remoção
arvore.listar_produtos()
