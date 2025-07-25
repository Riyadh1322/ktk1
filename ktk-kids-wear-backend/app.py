from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '1322'  # Replace with a secure key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ktk_kids_wear.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

# Initialize database
db.create_all()

# Create an admin user
admin = User(username="admin", password="admin123")
db.session.add(admin)
db.session.commit()
print("Admin user created!")

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            if username == "admin":  # Check if the user is admin
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form.get('quantity', 1))
        user = User.query.filter_by(username=session['user']).first()
        cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return redirect(url_for('cart'))

    user = User.query.filter_by(username=session['user']).first()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    products = [(item, Product.query.get(item.product_id)) for item in cart_items]
    return render_template('cart.html', products=products)

# Route to add a product to the database
@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    description = request.form['description']
    new_product = Product(name=name, price=price, description=description)
    db.session.add(new_product)
    db.session.commit()
    return "Product added successfully!"

# Route to retrieve all products
@app.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        } for product in products
    ]
    return {'products': product_list}

@app.route('/admin')
def admin_dashboard():
    if 'user' in session and session['user'] == "admin":
        return "Welcome to the Admin Dashboard!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    print("Flask app is running on http://127.0.0.1:5000/ (Press CTRL+C to quit)...")
