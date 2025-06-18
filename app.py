from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import handler
import admin

import handler.handler
from model.model import init_model


app = Flask(__name__)

app.config['SECRET_KEY'] = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

models = init_model(db)

admin.set_admin(app, db, models)

handler.handler.initialize_endpints(app, models, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)