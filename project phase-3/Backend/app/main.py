from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.app.main import Base, User, Product, Review, Order, OrderDetail
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Database URI
DATABASE_URI = 'sqlite:///electronics.sqlite'

# Setting up the SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# Creating a session maker
Session = sessionmaker(bind=engine)

# Initialize the database (create tables)
Base.metadata.create_all(engine)

@app.route('/')
def home():
    return 'Welcome to ETAM Electonics!'

# Route to create a new user
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    session = Session()
    new_user = User(username=data['username'], email=data['email'], role=data['role'])
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "User created successfully", "user": data}), 201

# Route to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    session = Session()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        price=data['price'],
        stock=data['stock'],
        seller_id=data['seller_id'],
        image_url=data['image_url']
    )
    session.add(new_product)
    session.commit()
    session.close()
    return jsonify({"message": "Product created successfully", "product": data}), 201

# Route to get products
@app.route('/products', methods=['GET'])
def get_products():
    session = Session()
    try:
        products = session.query(Product).all()
        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "stock": product.stock,
                "seller_id": product.seller_id,
                "image_url": product.image_url
            }
            for product in products
        ]
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# Route to delete a product
@app.route('/products/<string:name>', methods=['DELETE'])
def delete_product(name):
    session = Session()
    try:
        product = session.query(Product).filter_by(name=name).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        session.delete(product)
        session.commit()
        return jsonify({"message": "Product deleted successfully"}), 204
    except Exception as e:
        session.rollback()
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        session.close()

# Route to add a product review
@app.route('/product_reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    session = Session()
    new_review = Review(
        product_id=data['product_id'],
        user_id=data['user_id'],
        rating=data['rating'],
        review_text=data.get('review_text', ''),
        review_date=datetime.now()
    )
    session.add(new_review)
    session.commit()
    session.close()
    return jsonify({"message": "Review added successfully", "review": data}), 201

# Route to create an order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    session = Session()
    new_order = Order(
        user_id=data['user_id'],
        order_date=datetime.now(),
        total_amount=data['total_amount'],
        status=data['status']
    )
    session.add(new_order)
    session.commit()

    for item in data['order_details']:
        order_detail = OrderDetail(
            order_id=new_order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        session.add(order_detail)

    session.commit()
    session.close()

    return jsonify({"message": "Order created successfully", "order": data}), 201

if __name__ == '__main__':
    app.run(debug=True)
