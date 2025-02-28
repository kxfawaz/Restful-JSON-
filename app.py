from flask import Flask, jsonify, request, render_template
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

with app.app_context():
    connect_db(app)



# Create the database tables
with app.app_context():
    db.create_all()

    
    
@app.route('/')
def root():
    return render_template("index.html")
    
@app.route('/api/cupcakes')
def list_all():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)
   
    

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcakes=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(
        flavor = request.json['flavor'],
        rating = request.json['rating'],
        size = request.json['size'],
        image = request.json['image']
    )
   
    db.session.add(new_cupcake)
    db.session.commit()
    
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return(response_json,201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def patch_cupcakes(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.rating = request.json.get('rating',cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image = request.json.get('image',cupcake.image)
    
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcakes(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())
