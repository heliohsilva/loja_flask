from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required

def initialize_carrinho_endpoints(app, Carrinho, db):

    # Explicitly name the endpoint for the 'get_carrinhos' route
    @app.route('/carrinhos/', methods=['GET'], endpoint='get_all_carrinhos')
    @jwt_required
    def get_carrinhos():
        """
        Retrieves all shopping carts from the database.
        Requires JWT authentication.
        """
        carrinhos = Carrinho.query.all()
        return jsonify([carrinho.to_dict() for carrinho in carrinhos]), 200
    
    # Explicitly name the endpoint for the 'get_carrinho_by_id' route
    @app.route('/carrinho/<int:id>/', methods=['GET'], endpoint='get_carrinho_by_id')
    @jwt_required
    def get_carrinho(id):
        """
        Retrieves a single shopping cart by its ID.
        Returns a 404 if the cart is not found.
        Requires JWT authentication.
        """
        carrinho = Carrinho.query.get_or_404(id)
        return jsonify(carrinho.to_dict()), 200
    
    # Explicitly name the endpoint for the 'create_carrinho' route
    @app.route('/carrinho/', methods=['POST'], endpoint='create_new_carrinho')
    @jwt_required
    def create_carrinho():
        """
        Creates a new shopping cart.
        Expects JSON data with 'cliente_id'.
        Returns a 400 for invalid data.
        Requires JWT authentication.
        """
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Ensure 'cliente_id' is provided in the request data
        if 'cliente_id' not in data:
            return jsonify({'error': 'Cliente ID é obrigatório'}), 400

        novo_carrinho = Carrinho(cliente_id=data.get('cliente_id'))
        db.session.add(novo_carrinho)
        db.session.commit()
        
        return jsonify(novo_carrinho.to_dict()), 201
    
    @app.route('/carrinho/<int:id>/', methods=['PUT'], endpoint='update_carrinho')
    @jwt_required
    def update_carrinho(id):
        carrinho = Carrinho.query.get_or_404(id)
        data = request.get_json()
        
        if 'cliente_id' in data:
            carrinho.cliente_id = data['cliente_id']
        
        db.session.commit()
        
        return jsonify(carrinho.to_dict()), 200
    
    @app.route('/carrinho/<int:id>/', methods=['DELETE'], endpoint='delete_carrinho')
    @jwt_required
    def delete_carrinho(id):
        carrinho = Carrinho.query.get_or_404(id)
        db.session.delete(carrinho)
        db.session.commit()
        
        return jsonify({'message': 'Carrinho deletado com sucesso'}), 204
    
