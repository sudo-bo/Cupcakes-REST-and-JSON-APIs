"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(50), nullable=False)
    image = db.Column(db.Text, default="https://tinyurl.com/demo-cupcake")

    #  to populate users.html
    @classmethod
    def get_cupcakes(cls):
        return cls.query.all()
    
    # to provide info for user-detail.html
    @classmethod
    def find_cupcake(cls, id):
        return cls.query.get_or_404(id)

    
