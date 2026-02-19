from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Property
import os

app = Flask(__name__)
CORS(app)

# Configure SQLite database (Support local dev and Render persistent disks)
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = '/data'
if os.path.exists(data_dir):
    db_path = os.path.join(data_dir, 'properties.db')
else:
    db_path = os.path.join(basedir, 'properties.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure database tables are created in production (gunicorn bypasses __main__)
with app.app_context():
    db.create_all()

@app.route('/api/properties', methods=['GET'])
def get_properties():
    query = Property.query

    # Filters
    city = request.args.get('city')
    prop_type = request.args.get('type')
    max_budget = request.args.get('max_budget', type=int)

    if city:
        query = query.filter(Property.city == city)
    if prop_type:
        query = query.filter(Property.type == prop_type)
    if max_budget is not None:
        query = query.filter(Property.price <= max_budget)

    properties = query.all()
    return jsonify([p.to_dict() for p in properties])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
