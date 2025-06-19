from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import datetime

def initialize_auth_endpoints(app, Cliente, db):
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'error': 'Dados inválidos'}), 400
        
        existing_user = Cliente.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Usuário já existe'}), 400
        
        new_user = Cliente(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            email=data.get('email'),
            endereco=data.get('endereco'),
            telefone=data.get('telefone'),
        )

        new_user.set_password(data['senha'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário registrado com sucesso'}), 201
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Usando o modelo do dicionário models em vez de importação direta
        user = Cliente.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['senha']):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"msg": "Bad username or password"}), 401
        
    
    
