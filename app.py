"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, request, jsonify, abort
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = False # can change when needed

app.config['SECRET_KEY'] = 'development key'  # Needed for Flask sessions and debug toolbar
# toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect('/api/cupcakes')

@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = Cupcake.get_cupcakes()
    cupcakes_list = [{"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image} for cupcake in cupcakes]

    return jsonify(cupcakes=cupcakes_list)

@app.route('/api/cupcakes/<int:id>')
def get_cucpake_info(id):
    cupcake = Cupcake.find_cupcake(id)
    if cupcake:
        cupcake_info = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
        return jsonify(cupcakes=cupcake_info)
    else:
        return jsonify(error="Cupcake not found"), 404


@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():

    data = request.get_json()
    if data.get('flavor') and data.get('size') and data.get('rating'):
        new_cupcake = Cupcake(
            flavor=data['flavor'], 
            size=data['size'], 
            rating=data['rating'], 
            image=data.get('image')
        )
        db.session.add(new_cupcake)
        db.session.commit()

        new_cupcake_json = {"id": new_cupcake.id, "flavor": new_cupcake.flavor, "size": new_cupcake.size, "rating": new_cupcake.rating, "image": new_cupcake.image}
        return jsonify(cupcake=new_cupcake_json), 201
    else:
        return jsonify({"error": "Wrong info. Try again"})
   
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    data = request.get_json()
    cupcake = Cupcake.find_cupcake(id)

    if 'flavor' in data:
        cupcake['flavor'] = data['flavor'], 
    if 'size' in data:
        cupcake['size'] = data['size'], 
    if 'rating' in data:
        cupcake['rating'] = data['rating']
    if 'image' in data:
        cupcake['rating'] = data.get('image')

        db.session.commit()

        new_cupcake_json = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
        return jsonify(cupcake=new_cupcake_json), 200
    
@app.route('/api/cupcakes/<int:id>/delete', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.find_cupcake(id)
    deleted_cupcake_json = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
    
    db.session.remove(cupcake)
    db.session.commit()

    return jsonify(deleted_cupcake_json), 200