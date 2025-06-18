from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, request, jsonify
import handler

import handler.handler
from model.model import init_model


app = Flask(__name__)

app.config['SECRET_KEY'] = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

models = init_model(db)

admin = Admin(app, name='loja flask admin', template_mode='bootstrap3')

admin.add_view(ModelView(models["Cliente"], db.session))
admin.add_view(ModelView(models["Categoria"], db.session))
admin.add_view(ModelView(models["Produto"], db.session))
admin.add_view(ModelView(models["Pedido"], db.session))
admin.add_view(ModelView(models["ItemPedido"], db.session))
admin.add_view(ModelView(models["Carrinho"], db.session))
admin.add_view(ModelView(models["ItemCarrinho"], db.session))
admin.add_view(ModelView(models["Review"], db.session))
admin.add_view(ModelView(models["Pagamento"], db.session))

handler.handler.initialize_endpints(app, models, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)