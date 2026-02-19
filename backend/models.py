from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)  # "Tel Aviv" or "Holon"
    type = db.Column(db.String(20), nullable=False)  # "Rent" or "Buy"
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'city': self.city,
            'type': self.type,
            'price': self.price,
            'image_url': self.image_url
        }
