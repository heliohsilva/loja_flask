from flask import Blueprint, request, jsonify
import handler

app = Blueprint('app', __name__)

@app.route('/cliente', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        cliente = handler.cliente.create_cliente(data)
        return jsonify(cliente), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    try:
        cliente = handler.cliente.get_cliente(id)
        if not cliente:
            return jsonify({"error": "Cliente not found"}), 404
        return jsonify(cliente), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/cliente/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        cliente = handler.cliente.update_cliente(id, data)
        if not cliente:
            return jsonify({"error": "Cliente not found"}), 404
        return jsonify(cliente), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cliente/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        success = handler.cliente.delete_cliente(id)
        if not success:
            return jsonify({"error": "Cliente not found"}), 404
        return jsonify({"message": "Cliente deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/clientes', methods=['GET'])
def list_clientes():
    try:
        clientes = handler.cliente.list_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500