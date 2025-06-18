from flask import jsonify
from flask import request

def initialize_carrinho_endpoints(app, Carrinho, db):

    @app.route('/carrinhos/', methods=['GET'])
    def get_carrinhos():
        carrinhos = Carrinho.query.all()
        return jsonify([carrinho.to_dict() for carrinho in carrinhos]), 200
    
    @app.route('/carrinho/<int:id>/', methods=['GET'])
    def get_carrinho(id):
        carrinho = Carrinho.query.get_or_404(id)
        return jsonify(carrinho.to_dict()), 200
    
    @app.route('/carrinho/', methods=['POST'])
    def create_carrinho():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        novo_carrinho = Carrinho(cliente_id=data.get('cliente_id'))
        db.session.add(novo_carrinho)
        db.session.commit()
        
        return jsonify(novo_carrinho.to_dict()), 201
    
    @app.route('/carrinho/<int:id>/', methods=['PUT'])
    def update_carrinho(id):
        carrinho = Carrinho.query.get_or_404(id)
        data = request.get_json()
        
        if 'cliente_id' in data:
            carrinho.cliente_id = data['cliente_id']
        
        db.session.commit()
        
        return jsonify(carrinho.to_dict()), 200
    
    @app.route('/carrinho/<int:id>/', methods=['DELETE'])
    def delete_carrinho(id):
        carrinho = Carrinho.query.get_or_404(id)
        db.session.delete(carrinho)
        db.session.commit()
        
        return jsonify({'message': 'Carrinho deletado com sucesso'}), 204
    
