from . import carrinho, pedido, cliente , produto , pagamento, categoria, review, auth
from flask import request, jsonify
import jwt



def initialize_endpints(app, models, db):

    @app.route('/', methods=['GET'])
    def index():
        return "Welcome to the flask store API!"

    carrinho.initialize_carrinho_endpoints(app, models["Carrinho"], db)
    pedido.initialize_pedido_endpoints(app, models["Pedido"], db)
    cliente.initialize_cliente_endpoints(app, models["Cliente"], db)
    produto.initialize_produto_endpoints(app, models["Produto"], models["Categoria"], db)
    pagamento.initialize_pagamento_endpoints(app, models["Pagamento"], db)
    categoria.initialize_categoria_endpoints(app, models["Categoria"], db)
    review.initialize_review_endpoints(app, models["Review"], db)
    auth.initialize_auth_endpoints(app, models["Cliente"], db)


