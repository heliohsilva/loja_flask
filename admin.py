from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form import ImageUploadField



class ClienteView(ModelView):
    column_list = ['id', 'first_name', 'last_name', 'email', 'endereco', 'telefone', 'data_cadastro', 'pedidos', 'carrinho', 'reviews']
    column_labels = {
        'first_name': 'Nome',
        'last_name': 'Sobrenome',
        'endereco': 'Endereço',
        'telefone': 'Telefone',
        'data_cadastro': 'Data de Cadastro',
        'pedidos': 'Pedidos',
        'carrinho': 'Carrinho',
        'reviews': 'Avaliações'
    }
    form_excluded_columns = ['pedidos', 'carrinho', 'reviews', 'data_cadastro']
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_filters = ['data_cadastro', 'endereco']



class CategoriaView(ModelView):
    column_list = ['id', 'nome']
    column_labels = {
        'nome': 'Nome da Categoria'
    }
    form_columns = ['nome']
    column_searchable_list = ['nome']



class ProdutoView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model["Produto"], session, **kwargs)
        self.categoria_model = model["Categoria"]

    def get_categoria_model(self):
        return self.categoria_model

    column_list = ['id', 'nome', 'descricao', 'preco', 'estoque', 'imagem', 'categorias']
    column_labels = {
        'nome': 'Nome do Produto',
        'descricao': 'Descrição',
        'preco': 'Preço',
        'estoque': 'Estoque',
        'imagem': 'Imagem',
        'categorias': 'Categorias'
    }
    form_excluded_columns = ['itens_pedido', 'itens_carrinho', 'reviews']
    column_searchable_list = ['nome', 'descricao']
    column_filters = ['preco', 'estoque', 'categorias']
    
    form_overrides = {
        'imagem': ImageUploadField,
        'categorias': QuerySelectMultipleField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        # Configure categorias field
        form.categorias.query_factory = lambda: self.session.query(self.categoria_model).all()
        form.categorias.get_label = lambda c: c.nome
        # Configure image upload field
        form.imagem.base_path = 'media/uploads'
        form.imagem.relative_path = 'uploads'
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        # Configure categorias field
        form.categorias.query_factory = lambda: self.session.query(self.categoria_model).all()
        form.categorias.get_label = lambda c: c.nome
        # Configure image upload field
        form.imagem.base_path = 'media/uploads'
        form.imagem.relative_path = 'uploads'
        return form



class PedidoView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model["Pedido"], session, **kwargs)
        self.cliente_model = model["Cliente"]

    column_list = ['id', 'cliente', 'data', 'status', 'total', 'itens', 'pagamento']
    column_labels = {
        'cliente': 'Cliente',
        'data': 'Data do Pedido',
        'status': 'Status',
        'total': 'Total',
        'itens': 'Itens do Pedido',
        'pagamento': 'Pagamento'
    }
    form_excluded_columns = ['itens', 'pagamento']
    column_filters = ['status', 'data', 'cliente']
    column_searchable_list = ['status']
    
    form_overrides = {
        'cliente': QuerySelectField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        return form



class CarrinhoView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model["Carrinho"], session, **kwargs)
        self.cliente_model = model["Cliente"]

    column_list = ['id', 'cliente', 'itens']
    column_labels = {
        'cliente': 'Cliente',
        'itens': 'Itens do Carrinho',
    }
    form_excluded_columns = ['itens']
    
    form_overrides = {
        'cliente': QuerySelectField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        return form



class PagamentoView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model["Pagamento"], session, **kwargs)
        self.pedido_model = model["Pedido"]

    column_list = ['id', 'pedido', 'metodo_pagamento', 'status', 'data']
    column_labels = {
        'pedido': 'Pedido',
        'metodo_pagamento': 'Método de Pagamento',
        'status': 'Status do Pagamento',
        'data': 'Data do Pagamento'
    }
    column_filters = ['metodo_pagamento', 'status', 'data']
    column_searchable_list = ['metodo_pagamento', 'status']
    
    form_overrides = {
        'pedido': QuerySelectField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, 'pedido'):
            form.pedido.query_factory = lambda: self.session.query(self.pedido_model).all()
            form.pedido.get_label = lambda p: f"Pedido #{p.id} - {p.cliente.first_name if p.cliente else 'N/A'}"
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, 'pedido'):
            form.pedido.query_factory = lambda: self.session.query(self.pedido_model).all()
            form.pedido.get_label = lambda p: f"Pedido #{p.id} - {p.cliente.first_name if p.cliente else 'N/A'}"
        return form



class ReviewView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model["Review"], session, **kwargs)
        self.cliente_model = model["Cliente"]
        self.produto_model = model["Produto"]

    column_list = ['id', 'cliente', 'produto', 'nota', 'comentario', 'data']
    column_labels = {
        'cliente': 'Cliente',
        'produto': 'Produto',
        'nota': 'Avaliação',
        'comentario': 'Comentário',
        'data': 'Data'
    }
    column_filters = ['nota', 'data', 'cliente', 'produto']
    column_searchable_list = ['comentario']
    
    form_overrides = {
        'cliente': QuerySelectField,
        'produto': QuerySelectField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        if hasattr(form, 'produto'):
            form.produto.query_factory = lambda: self.session.query(self.produto_model).all()
            form.produto.get_label = lambda p: p.nome
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if hasattr(form, 'cliente'):
            form.cliente.query_factory = lambda: self.session.query(self.cliente_model).all()
            form.cliente.get_label = lambda c: f"{c.first_name} {c.last_name}"
        if hasattr(form, 'produto'):
            form.produto.query_factory = lambda: self.session.query(self.produto_model).all()
            form.produto.get_label = lambda p: p.nome
        return form



def set_admin(app, db, models):
    admin = Admin(app, name='Loja Flask Admin', template_mode='bootstrap3')
    admin.add_view(ClienteView(models["Cliente"], db.session))
    admin.add_view(CategoriaView(models["Categoria"], db.session))
    admin.add_view(ProdutoView(models, db.session))
    admin.add_view(PedidoView(models, db.session))
    admin.add_view(CarrinhoView(models, db.session))
    admin.add_view(ReviewView(models, db.session))
    admin.add_view(PagamentoView(models, db.session))
    return admin