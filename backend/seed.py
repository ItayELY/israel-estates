from app import app
from models import db, Property

# 10 Tel Aviv, 10 Holon
# Mix of Rent/Buy
mock_data = [
    # Tel Aviv - Rent
    {"title": "Luxury Apartment on Rothschild", "description": "Beautiful 3-bedroom apartment with a city view.", "city": "Tel Aviv", "type": "Rent", "price": 12000, "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80"},
    {"title": "Cozy Studio in Florentin", "description": "Perfect for singles or young couples.", "city": "Tel Aviv", "type": "Rent", "price": 5500, "image_url": "https://images.unsplash.com/photo-1502672260266-1c1f5523774d?w=800&q=80"},
    {"title": "Modern Loft near the Beach", "description": "Spacious loft just 5 minutes from the sea.", "city": "Tel Aviv", "type": "Rent", "price": 9000, "image_url": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800&q=80"},
    {"title": "Renovated 2BR in Old North", "description": "Quiet street, fully renovated.", "city": "Tel Aviv", "type": "Rent", "price": 8500, "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80"},
    {"title": "Penthouse with Huge Balcony", "description": "Top floor with amazing views.", "city": "Tel Aviv", "type": "Rent", "price": 18000, "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80"},
    # Tel Aviv - Buy
    {"title": "Prime Location 4BR Apartment", "description": "Great investment opportunity in the center.", "city": "Tel Aviv", "type": "Buy", "price": 6500000, "image_url": "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=800&q=80"},
    {"title": "New Build Neve Tzedek", "description": "Brand new luxury property.", "city": "Tel Aviv", "type": "Buy", "price": 8200000, "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80"},
    {"title": "Compact 1BR for Investment", "description": "High yield potential.", "city": "Tel Aviv", "type": "Buy", "price": 2800000, "image_url": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&q=80"},
    {"title": "Bauhaus Classic", "description": "Historic building, fully restored.", "city": "Tel Aviv", "type": "Buy", "price": 7500000, "image_url": "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=80"},
    {"title": "Sea View Duplex", "description": "Wake up to the sound of waves.", "city": "Tel Aviv", "type": "Buy", "price": 12000000, "image_url": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=80"},

    # Holon - Rent
    {"title": "Family Home near Park Peres", "description": "Spacious 4-bedroom apartment, great for families.", "city": "Holon", "type": "Rent", "price": 6500, "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80"},
    {"title": "New 3BR in Kiryat Ayalon", "description": "Includes parking and elevator.", "city": "Holon", "type": "Rent", "price": 5800, "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80"},
    {"title": "Upgraded Apartment on Sokolov", "description": "Central location, close to public transport.", "city": "Holon", "type": "Rent", "price": 4800, "image_url": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=800&q=80"},
    {"title": "Quiet 2BR with Sun Terrace", "description": "Well-lit and very quiet.", "city": "Holon", "type": "Rent", "price": 4200, "image_url": "https://images.unsplash.com/photo-1576941089067-2de3ce907869?w=800&q=80"},
    {"title": "Ground Floor with Garden", "description": "Private garden, pet friendly.", "city": "Holon", "type": "Rent", "price": 7000, "image_url": "https://images.unsplash.com/photo-1588880331179-bc9b9c4acadd?w=800&q=80"},
    # Holon - Buy
    {"title": "Premium 5BR Penthouse", "description": "Luxury living in Holon.", "city": "Holon", "type": "Buy", "price": 4500000, "image_url": "https://images.unsplash.com/photo-1600607687989-ce4d6d0ba91a?w=800&q=80"},
    {"title": "Spacious 4BR for Family", "description": "Near schools and parks.", "city": "Holon", "type": "Buy", "price": 2700000, "image_url": "https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?w=800&q=80"},
    {"title": "Renovated 3BR Investment", "description": "Currently rented out, good yield.", "city": "Holon", "type": "Buy", "price": 2100000, "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80"},
    {"title": "Brand New Project in H-300", "description": "Buy from contractor.", "city": "Holon", "type": "Buy", "price": 3200000, "image_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80"},
    {"title": "Cozy 2-Room Apartment", "description": "Perfect for a young couple.", "city": "Holon", "type": "Buy", "price": 1600000, "image_url": "https://images.unsplash.com/photo-1522771731535-61eea44365f5?w=800&q=80"},
]

def seed_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        for data in mock_data:
            prop = Property(**data)
            db.session.add(prop)
        
        db.session.commit()
        print("Database seeded with 20 mock properties!")

if __name__ == '__main__':
    seed_db()
