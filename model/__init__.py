from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .model import init_model
_models = init_model(db)

# exponha o dict de models diretamente
models = _models

__all__ = ['db', 'models']
