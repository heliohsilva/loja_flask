from flask import Flask
from flask_login import LoginManager, current_user
from flask_jwt_extended import JWTManager

import handler.handler
import admin
from model import db, models
from views import view as view_routes

from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT (se usar)
jwt = JWTManager(app)

# WTF
csrf = CSRFProtect()
csrf.init_app(app)

# 1) INICIA o DB
db.init_app(app)

# 2) ADMIN
admin.set_admin(app, db, models)

# 3) LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'view.login'

@login_manager.user_loader
def load_user(user_id):
    return models['Cliente'].query.get(int(user_id))

@app.context_processor
def inject_user():
    # Injeta current_user no template como 'user'
    return dict(user=current_user)

# 4) FRONTEND
app.register_blueprint(view_routes)

# 5) API HANDLERS
handler.handler.initialize_endpints(app, models, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
