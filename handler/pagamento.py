from flask import jsonify
from flask import request

def initialize_pagamento_endpoints(app, Pagamento, db):

    @app.route('/pagamentos/', methods=['GET'])
    def get_pagamentos():
        pagamentos = Pagamento.query.all()
        print(pagamentos)
        return jsonify([pagamento.to_dict() for pagamento in pagamentos]), 200
    
    @app.route('/pagamento/<int:id>/', methods=['GET'])
    def get_pagamento(id):
        pagamento = Pagamento.query.get_or_404(id)
        return jsonify(pagamento.to_dict()), 200
    
    @app.route('/pagamento/', methods=['POST'])
    def create_pagamento():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        novo_pagamento = Pagamento(
            pedido_id=data.get('pedido_id'),
            valor=data.get('valor'),
            metodo_pagamento=data.get('metodo_pagamento')
        )
        
        db.session.add(novo_pagamento)
        db.session.commit()
        
        return jsonify(novo_pagamento.to_dict()), 201
    
    @app.route('/pagamento/<int:id>/', methods=['PUT'])
    def update_pagamento(id):
        pagamento = Pagamento.query.get_or_404(id)
        data = request.get_json()
        
        if 'pedido_id' in data:
            pagamento.pedido_id = data['pedido_id']
        if 'valor' in data:
            pagamento.valor = data['valor']
        if 'metodo_pagamento' in data:
            pagamento.metodo_pagamento = data['metodo_pagamento']
        
        db.session.commit()
        
        return jsonify(pagamento.to_dict()), 200
    
    @app.route('/pagamento/<int:id>/', methods=['DELETE'])
    def delete_pagamento(id):
        pagamento = Pagamento.query.get_or_404(id)
        db.session.delete(pagamento)
        db.session.commit()
        
        return jsonify({'message': 'Pagamento deletado com sucesso'}), 204