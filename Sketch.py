#Sketch do trabalho python sistema de vendas

class Produto:
    def __init__(self, id_prod, nome, preco):
        self.id_prod = id_prod
        self.nome = nome
        self.preco = preco

class Venda:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
        self.total = produto.preco * quantidade

class NodoProduto:
    def __init__(self, produto):
        self.produto = produto
        self.vendas = []  # Lista de vendas para este produto
        self.esquerda = None
        self.direita = None

class ArvoreProdutos:
    def __init__(self):
        self.raiz = None

    def inserir_produto(self, produto):
        if self.raiz is None:
            self.raiz = NodoProduto(produto)
        else:
            self._inserir(self.raiz, produto)

    def _inserir(self, nodo, produto):
        if produto.id_prod < nodo.produto.id_prod:
            if nodo.esquerda is None:
                nodo.esquerda = NodoProduto(produto)
            else:
                self._inserir(nodo.esquerda, produto)
        elif produto.id_prod > nodo.produto.id_prod:
            if nodo.direita is None:
                nodo.direita = NodoProduto(produto)
            else:
                self._inserir(nodo.direita, produto)
        else:
            # Produto jÃ¡ existe, pode atualizar ou ignorar
            pass

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
        self._em_ordem(self.raiz)

    def _em_ordem(self, nodo):
        if nodo:
            self._em_ordem(nodo.esquerda)
            print(f"Produto ID: {nodo.produto.id_prod}, Nome: {nodo.produto.nome}, PreÃ§o: R${nodo.produto.preco:.2f}")
            self._em_ordem(nodo.direita)

# Lista de vendas
lista_vendas = []

# Exemplo de uso
# Criando produtos
produto1 = Produto(1, "Camiseta", 50.0)
produto2 = Produto(2, "CalÃ§a", 120.0)

# Criando Ã¡rvore de produtos
arvore = ArvoreProdutos()
arvore.inserir_produto(produto1)
arvore.inserir_produto(produto2)

# Registrando vendas
venda1 = Venda(produto1, 2)
venda2 = Venda(produto2, 1)

# Adicionando vendas Ã  lista geral
lista_vendas.append(venda1)
lista_vendas.append(venda2)

# Associando vendas ao produto na Ã¡rvore
nodo_produto1 = arvore.buscar_produto(1)
if nodo_produto1:
    nodo_produto1.vendas.append(venda1)

nodo_produto2 = arvore.buscar_produto

