from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import db                # vem de model/__init__.py
from model import models

view = Blueprint('view', __name__)

Cliente = models['Cliente']
Categoria = models['Categoria']
Produto = models['Produto']
Pedido = models['Pedido']
ItemPedido = models['ItemPedido']
Carrinho = models['Carrinho']
ItemCarrinho = models['ItemCarrinho']
Pagamento = models['Pagamento']
Review = models['Review']

@view.route('/')
def index():
    query = request.args.get('search', '')
    categoria_id = request.args.get('categoria')

    produtos = Produto.query
    categorias = Categoria.query.all()

    if query:
        produtos = produtos.filter(Produto.nome.ilike(f'%{query}%'))

    if categoria_id:
        produtos = produtos.filter(Produto.categoria_id == categoria_id)

    produtos = produtos.all()

    return render_template('index.html', produtos=produtos, categorias=categorias, query_original=query)

@view.route('/produto/<int:id>/')
def product(id):
    produto = Produto.query.get_or_404(id)
    comentarios = Review.query.filter_by(produto_id=id).order_by(Review.data.desc()).all()
    return render_template('product.html', produto=produto, comentarios=comentarios)

@view.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome  = request.form.get('nome', '')
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')
        endereco = request.form.get('endereco', '')
        telefone = request.form.get('telefone', '')

        # agora senha e confirmar_senha são sempre strings
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
            return redirect(url_for('view.cadastro'))

        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'error')
            return redirect(url_for('view.cadastro'))

        if Cliente.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'error')
            return redirect(url_for('view.cadastro'))

        # cria o Cliente e seta a senha hash
        novo = Cliente(
            username=email,
            email=email,
            first_name=nome,
            last_name='',
        )
        novo.set_password(senha)
        novo.endereco = endereco
        novo.telefone = telefone

        db.session.add(novo)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.')
        return render_template('login.html')

    return render_template('login.html')

@view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')  # garante string, nunca None

        user = Cliente.query.filter_by(email=email).first()
        print(user)

        # usa o método definido no model
        if user and user.check_password(senha):
            login_user(user)
            flash('Login realizado com sucesso!')
            return redirect(url_for('view.index'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('view.login'))

    return render_template('login.html')

@view.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('views.index'))

@view.route('/minha-conta')
@login_required
def minha_conta():
    cliente = Cliente.query.filter_by(id=current_user.id).first()
    return render_template('minha_conta.html', user=cliente)

@view.route('/adicionar_comentario/<int:id>/', methods=['POST'])
@login_required
def adicionar_comentario(id):
    texto = request.form.get('texto')
    nota = int(request.form.get('nota', 5))

    produto = Produto.query.get_or_404(id)

    review = Review(produto_id=produto.id, cliente_id=current_user.cliente.id, comentario=texto, nota=nota)
    db.session.add(review)
    db.session.commit()

    return redirect(url_for('views.product', id=id))

@view.route('/carrinho')
@login_required
def carrinho():
    carrinho = Carrinho.query.filter_by(cliente_id=current_user.cliente.id).first()

    if not carrinho:
        carrinho = Carrinho(cliente_id=current_user.cliente.id)
        db.session.add(carrinho)
        db.session.commit()

    items = ItemCarrinho.query.filter_by(carrinho_id=carrinho.id).all()
    valor_total = sum(item.quantidade * item.preco for item in items)

    return render_template('carrinho.html', items=items, valor_total=valor_total)

@view.route('/adicionar_ao_carrinho/<int:id>/')
@login_required
def adicionar_ao_carrinho(id):
    produto = Produto.query.get_or_404(id)

    carrinho = Carrinho.query.filter_by(cliente_id=current_user.cliente.id).first()
    if not carrinho:
        carrinho = Carrinho(cliente_id=current_user.cliente.id)
        db.session.add(carrinho)
        db.session.commit()

    item = ItemCarrinho.query.filter_by(carrinho_id=carrinho.id, produto_id=id).first()

    if item:
        item.quantidade += 1
    else:
        item = ItemCarrinho(carrinho_id=carrinho.id, produto_id=id, quantidade=1, preco=produto.preco)
        db.session.add(item)

    db.session.commit()

    return redirect(url_for('views.carrinho'))

@view.route('/pagamento')
@login_required
def pagamento():
    carrinho = Carrinho.query.filter_by(cliente_id=current_user.cliente.id).first()
    if not carrinho or not carrinho.itens:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('views.carrinho'))

    valor_total = sum(item.quantidade * item.preco for item in carrinho.itens)
    return render_template('pagamento.html', valor_total=valor_total)

@view.route('/pos_pagamento', methods=['POST'])
@login_required
def pos_pagamento():
    carrinho = Carrinho.query.filter_by(cliente_id=current_user.cliente.id).first()
    if not carrinho or not carrinho.itens:
        flash('Não há itens no carrinho.', 'error')
        return redirect(url_for('views.index'))

    pedido = Pedido(cliente_id=current_user.cliente.id)
    db.session.add(pedido)
    db.session.commit()

    for item in carrinho.itens:
        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco=item.preco
        )
        db.session.add(item_pedido)

    db.session.delete(carrinho)
    db.session.commit()

    flash('Pedido realizado com sucesso!')
    return render_template('thanks.html')

@view.route('/thanks')
def thanks():
    return render_template('thanks.html')