from flask import jsonify
from flask import request

def initialize_pedido_endpoints(app, Pedido, db):

    @app.route('/pedidos/', methods=['GET'])
    def get_pedidos():
        pedidos = Pedido.query.all()
        print(pedidos)
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    
    @app.route('/pedido/<int:id>/', methods=['GET'])
    def get_pedido(id):
        pedido = Pedido.query.get_or_404(id)
        return jsonify(pedido.to_dict()), 200
    
    @app.route('/pedido/', methods=['POST'])
    def create_pedido():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        novo_pedido = Pedido(
            cliente_id=data.get('cliente_id'),
            status=data.get('status'),
            total=data.get('total')
        )
        
        db.session.add(novo_pedido)
        db.session.commit()
        
        return jsonify(novo_pedido.to_dict()), 201
    
    @app.route('/pedido/<int:id>/', methods=['PUT'])
    def update_pedido(id):
        pedido = Pedido.query.get_or_404(id)
        data = request.get_json()
        
        if 'cliente_id' in data:
            pedido.cliente_id = data['cliente_id']
        if 'status' in data:
            pedido.status = data['status']
        if 'total' in data:
            pedido.total = data['total']
        
        db.session.commit()
        
        return jsonify(pedido.to_dict()), 200
    
    @app.route('/pedido/<int:id>/', methods=['DELETE'])
    def delete_pedido(id):
        pedido = Pedido.query.get_or_404(id)
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({'message': 'Pedido deletado com sucesso'}), 204
    