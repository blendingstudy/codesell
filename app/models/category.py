from app import db
from app.models import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Category {self.name}>'