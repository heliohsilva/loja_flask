from datetime import datetime

def init_model(db):

    produto_categoria = db.Table('produto_categoria',
        db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
        db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
    )


    class Cliente(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(120), nullable=False)
        endereco = db.Column(db.Text)
        telefone = db.Column(db.String(15))
        data_cadastro = db.Column(db.Date, default=datetime.utcnow)
        
        pedidos = db.relationship('Pedido', backref='cliente', lazy=True)
        carrinho = db.relationship('Carrinho', backref='cliente', uselist=False)
        reviews = db.relationship('Review', backref='cliente', lazy=True)
        
        def __str__(self):
            return f"{self.first_name} <{self.email}>"
        
        def to_dict(self):
            return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'endereco': self.endereco,
                'telefone': self.telefone,
                'data_cadastro': self.data_cadastro.strftime('%Y-%m-%d')
            }

    class Categoria(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(50), nullable=False)
        
        def __str__(self):
            return self.nome
        
        def to_dict(self):
            return {
                'id': self.id,
                'nome': self.nome
            }

    class Produto(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(50), nullable=False)
        descricao = db.Column(db.Text)
        preco = db.Column(db.Numeric(10, 2), nullable=False)
        estoque = db.Column(db.Integer, default=0)
        imagem = db.Column(db.String(200), nullable=True) 
        
        categorias = db.relationship('Categoria', secondary=produto_categoria, 
                                    backref=db.backref('produtos', lazy='dynamic'))
        itens_pedido = db.relationship('ItemPedido', backref='produto', lazy=True)
        itens_carrinho = db.relationship('ItemCarrinho', backref='produto', lazy=True)
        reviews = db.relationship('Review', backref='produto', lazy=True)
        
        def __str__(self):
            return f"{self.nome} - R${self.preco}"
        
        def em_estoque(self):
            return self.estoque > 0
        
        def star_rating(self):
            if not self.reviews:
                return 5
            return round(sum(review.nota for review in self.reviews) / len(self.reviews))
        
        def count_reviews(self):
            return len(self.reviews)
        
        def to_dict(self):
            return {
                'id': self.id,
                'nome': self.nome,
                'descricao': self.descricao,
                'preco': str(self.preco),
                'estoque': self.estoque,
                'imagem': self.imagem,
                'categorias': [categoria.nome for categoria in self.categorias],
                'star_rating': self.star_rating(),
                'count_reviews': self.count_reviews()
            }

    class Pedido(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
        data = db.Column(db.Date, default=datetime.utcnow)
        status = db.Column(db.String(20), default='pendente')
        
        itens = db.relationship('ItemPedido', backref='pedido', lazy=True)
        pagamento = db.relationship('Pagamento', backref='pedido', uselist=False)
        
        @property
        def total(self):
            return sum(item.preco_unitario * item.quantidade for item in self.itens)
        
        def __str__(self):
            return f"Pedido #{self.id} - Cliente: {self.cliente.user.last_name} - Status: {self.status}"
        
        def to_dict(self):
            return {
                'id': self.id,
                'cliente_id': self.cliente_id,
                'data': self.data.strftime('%Y-%m-%d'),
                'status': self.status,
                'total': str(self.total),
                'itens': [item.to_dict() for item in self.itens]
            }

    class ItemPedido(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
        produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
        quantidade = db.Column(db.Integer, nullable=False)
        preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
        
        def __str__(self):
            return f"Produto: {self.produto.nome} - Quantidade: {self.quantidade}"
        
        def to_dict(self):
            return {
                'id': self.id,
                'pedido_id': self.pedido_id,
                'produto_id': self.produto_id,
                'quantidade': self.quantidade,
                'preco_unitario': str(self.preco_unitario),
                'produto_nome': self.produto.nome
            }

    class Carrinho(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
        data_criacao = db.Column(db.Date, default=datetime.utcnow)
        status = db.Column(db.String(20), default='ativo')
        
        itens = db.relationship('ItemCarrinho', backref='carrinho', lazy=True)
        
        def __str__(self):
            return f"Carrinho #{self.id} - Cliente: {self.cliente.user.first_name} - Status: {self.status}"
        
        def total(self):
            return sum(item.produto.preco * item.quantidade for item in self.itens)
        
        def to_dict(self):
            return {
                'id': self.id,
                'cliente_id': self.cliente_id,
                'data_criacao': self.data_criacao.strftime('%Y-%m-%d'),
                'status': self.status,
                'total': str(self.total()),
                'itens': [item.to_dict() for item in self.itens]
            }

    class ItemCarrinho(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinho.id'), nullable=False)
        produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
        preco = db.Column(db.Numeric(10, 2), default=0)
        quantidade = db.Column(db.Integer, nullable=False)
        
        def __str__(self):
            return f"Produto: {self.produto.nome} - Quantidade: {self.quantidade}"
        
        def to_dict(self):
            return {
                'id': self.id,
                'carrinho_id': self.carrinho_id,
                'produto_id': self.produto_id,
                'preco': str(self.preco),
                'quantidade': self.quantidade,
                'produto_nome': self.produto.nome
            }

    class Pagamento(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
        data = db.Column(db.Date, default=datetime.utcnow)
        valor = db.Column(db.Numeric(10, 2), nullable=False)
        status = db.Column(db.String(20), default='pendente')
        metodo_pagamento = db.Column(db.String(25))
        
        def __str__(self):
            return f"Pagamento - Pedido #{self.pedido.id} - Valor: R${self.valor}"
        
        def to_dict(self):
            return {
                'id': self.id,
                'pedido_id': self.pedido_id,
                'data': self.data.strftime('%Y-%m-%d'),
                'valor': str(self.valor),
                'status': self.status,
                'metodo_pagamento': self.metodo_pagamento
            }

    class Review(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
        produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
        nota = db.Column(db.Integer, nullable=False)
        comentario = db.Column(db.Text)
        data = db.Column(db.Date, default=datetime.utcnow)
        
        def __str__(self):
            return f"Review - Produto: {self.produto.nome} - Nota: {self.nota}"
        
        def to_dict(self):
            return {
                'id': self.id,
                'cliente_id': self.cliente_id,
                'produto_id': self.produto_id,
                'nota': self.nota,
                'comentario': self.comentario,
                'data': self.data.strftime('%Y-%m-%d')
            }
        
    return {
        'Cliente': Cliente,
        'Categoria': Categoria,
        'Produto': Produto,
        'Pedido': Pedido,
        'ItemPedido': ItemPedido,
        'Carrinho': Carrinho,
        'ItemCarrinho': ItemCarrinho,
        'Pagamento': Pagamento,
        'Review': Review
    }