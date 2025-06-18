from flask import jsonify
from flask import request

def initialize_categoria_endpoints(app, Categoria, db):

    @app.route('/categorias/', methods=['GET'])
    def get_categorias():
        categorias = Categoria.query.all()
        print(categorias)
        return jsonify([categoria.to_dict() for categoria in categorias]), 200
    
    
    @app.route('/categoria/<int:id>/', methods=['GET'])
    def get_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        return jsonify(categoria.to_dict()), 200
    

    @app.route('/categoria/', methods=['POST'])
    def create_categoria():
        data = request.get_json()
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        nova_categoria = Categoria(nome=data['nome'])
        db.session.add(nova_categoria)
        db.session.commit()
        
        return jsonify(nova_categoria.to_dict()), 201
    
    @app.route('/categoria/<int:id>/', methods=['PUT'])
    def update_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        data = request.get_json()
        
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        categoria.nome = data['nome']
        db.session.commit()
        
        return jsonify(categoria.to_dict()), 200
    

    @app.route('/categoria/<int:id>/', methods=['DELETE'])
    def delete_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        db.session.delete(categoria)
        db.session.commit()
        
        return jsonify({'message': 'Categoria deletada com sucesso'}), 200