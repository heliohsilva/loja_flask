from flask import jsonify
from flask import request

def initialize_cliente_endpoints(app, Cliente, db):

    @app.route('/clientes/', methods=['GET'])
    def get_clientes():
        clientes = Cliente.query.all()
        print(clientes)
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    
    @app.route('/cliente/<int:id>/', methods=['GET'])
    def get_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        return jsonify(cliente.to_dict()), 200
    
    @app.route('/cliente/', methods=['POST'])
    def create_cliente():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        novo_cliente = Cliente(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            email=data.get('email'),
            endereco=data.get('endereco'),
            telefone=data.get('telefone'),
        )
        
        novo_cliente.set_password(data.get('senha', ''))

        db.session.add(novo_cliente)
        db.session.commit()
        
        return jsonify(novo_cliente.to_dict()), 201
    
    @app.route('/cliente/<int:id>/', methods=['PUT'])
    def update_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        data = request.get_json()
        
        if 'first_name' in data:
            cliente.first_name = data['first_name']
        if 'last_name' in data:
            cliente.last_name = data['last_name']
        if 'email' in data:
            cliente.email = data['email']
        if 'endereco' in data:
            cliente.endereco = data['endereco']
        if 'telefone' in data:
            cliente.telefone = data['telefone']
        
        if 'senha' in data:
            cliente.set_senha(data['senha'])
        
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 200
    
    @app.route('/cliente/<int:id>/', methods=['DELETE'])
    def delete_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({'message': 'Cliente deletado com sucesso'}), 204
    