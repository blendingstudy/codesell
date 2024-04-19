from app import db
from app.models import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('name', 'type', name='unique_category'),
    )

    def __init__(self, name, type, description=None):
        self.name = name
        self.type = type
        self.description = description

    def __repr__(self):
        return f'<Category {self.name} - {self.type}>'