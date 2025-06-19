from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form import ImageUploadField
from wtforms import PasswordField
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import redirect, url_for, current_app
from flask import jsonify

class ClienteView(ModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)
        self.model = model
    
    def is_accessible(self):
        try:
            jwt_required()(lambda: None)()  
            current_user_id = get_jwt_identity()
            user = self.model.query.get(current_user_id)
            return user and user.is_admin
        
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):

        return jsonify({'message': 'Acesso negado! Você não tem permissão para acessar esta página.'}), 403
    
    column_list = ['id', 'first_name', 'last_name', 'email', 'endereco', 'telefone', 'data_cadastro', 'senha']
    
    column_labels = {
        'first_name': 'Nome',
        'last_name': 'Sobrenome',
        'endereco': 'Endereço',
        'telefone': 'Telefone',
        'data_cadastro': 'Data de Cadastro',
        'senha': 'Senha'
    }
    
    form_excluded_columns = ['data_cadastro', 'senha']
    
    form_extra_fields = {
        'password': PasswordField('Senha')
    }
    
    def on_model_change(self, form, model, is_created):
        if hasattr(form, 'password') and form.password.data:
            model.set_password(form.password.data)

            form.password.data = ''
        super().on_model_change(form, model, is_created)
    
    def on_form_prefill(self, form, id):
        
        if hasattr(form, 'password'):
            form.password.data = ''
        return super().on_form_prefill(form, id)
    
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

    column_list = ['id', 'nome', 'descricao', 'preco', 'estoque', 'imagem', 'categorias', 'reviews']
    column_labels = {
        'nome': 'Nome do Produto',
        'descricao': 'Descrição',
        'preco': 'Preço',
        'estoque': 'Estoque',
        'imagem': 'Imagem',
        'categorias': 'Categorias',
        'reviews': 'Avaliação'
    }

    column_formatters = {
        'reviews': lambda v, c, m, p: f"{m.star_rating():.1f} ★" if m.star_rating() else "Sem avaliações"
    }

    form_excluded_columns = ['itens_pedido', 'itens_carrinho', 'reviews']
    column_searchable_list = ['nome', 'descricao']
    column_filters = ['preco', 'estoque', 'categorias', 'reviews']
    
    form_overrides = {
        'imagem': ImageUploadField,
        'categorias': QuerySelectMultipleField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.categorias.query_factory = lambda: self.session.query(self.categoria_model).all()
        form.categorias.get_label = lambda c: c.nome
        form.imagem.base_path = 'media/uploads'
        form.imagem.relative_path = 'uploads'
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.categorias.query_factory = lambda: self.session.query(self.categoria_model).all()
        form.categorias.get_label = lambda c: c.nome
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