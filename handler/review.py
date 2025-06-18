from flask import jsonify
from flask import request

def initialize_review_endpoints(app, Review, db):

    @app.route('/review/', methods=['GET'])
    def get_reviews():
        reviews = Review.query.all()
        print(reviews)
        return jsonify([review.to_dict() for review in reviews]), 200
    
    @app.route('/review/<int:id>/', methods=['GET'])
    def get_review(id):
        review = Review.query.get_or_404(id)
        return jsonify(review.to_dict()), 200
    
    @app.route('/review/', methods=['POST'])
    def create_review():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        novo_review = Review(
            produto_id=data.get('produto_id'),
            cliente_id=data.get('cliente_id'),
            rating=data.get('rating'),
            comentario=data.get('comentario')
        )
        
        db.session.add(novo_review)
        db.session.commit()
        
        return jsonify(novo_review.to_dict()), 201
    
    @app.route('/review/<int:id>/', methods=['PUT'])
    def update_review(id):
        review = Review.query.get_or_404(id)
        data = request.get_json()
        
        if 'produto_id' in data:
            review.produto_id = data['produto_id']
        if 'cliente_id' in data:
            review.cliente_id = data['cliente_id']
        if 'rating' in data:
            review.rating = data['rating']
        if 'comentario' in data:
            review.comentario = data['comentario']
        
        db.session.commit()
        
        return jsonify(review.to_dict()), 200
    
    @app.route('/review/<int:id>/', methods=['DELETE'])
    def delete_review(id):
        review = Review.query.get_or_404(id)
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deletado com sucesso'}), 204