"""Flask app for Cupcakes"""
# app.py
from flask import Flask, jsonify, request, render_template, redirect

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "your-secret-key-goes-here"

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Render the homepage with a form to add a new cupcake."""
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    return jsonify(cupcakes=[cupcake.serialize() for cupcake in cupcakes])

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with data from the request."""
    data = request.json
    cupcake = Cupcake(flavor=data['flavor'], size=data['size'], rating=data['rating'], image=data.get('image'))
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)
