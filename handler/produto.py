from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required

def initialize_produto_endpoints(app, Produto, Categoria, db):

    @app.route('/produtos/', methods=['GET'])
    def get_produtos():
        produtos = Produto.query.all()
        print(produtos)
        return jsonify([produto.to_dict() for produto in produtos]), 200
    
    @app.route('/produto/<int:id>/', methods=['GET'])
    def get_produto(id):
        produto = Produto.query.get_or_404(id)
        return jsonify(produto.to_dict()), 200
    
    @app.route('/produto/', methods=['POST'])
    def create_produto():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        categoria_id = data.get('id_categoria')
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                return jsonify({'error': 'Categoria não encontrada'}), 404
            

        novo_produto = Produto(
            nome=data.get('nome'),
            descricao=data.get('descricao'),
            preco=data.get('preco'),
            estoque=data.get('estoque'),
            imagem=data.get('url_image'),
        )

        novo_produto.categorias.append(categoria)
        
        db.session.add(novo_produto)
        db.session.commit()
        
        return jsonify(novo_produto.to_dict()), 201
    
    @app.route('/produto/<int:id>/', methods=['PUT'])
    def update_produto(id):
        produto = Produto.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome' in data:
            produto.nome = data['nome']
        if 'descricao' in data:
            produto.descricao = data['descricao']
        if 'preco' in data:
            produto.preco = data['preco']
        if 'estoque' in data:
            produto.estoque = data['estoque']
        
        db.session.commit()
        
        return jsonify(produto.to_dict()), 200
    
    @app.route('/produto/<int:id>/', methods=['DELETE'])
    def delete_produto(id):
        produto = Produto.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({'message': 'Produto deletado com sucesso'}), 204