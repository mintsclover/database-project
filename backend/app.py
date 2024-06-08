from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from models import db, Restaurant, Menu, User, Review, TodayMenu

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # 세션 암호화를 위한 비밀 키 설정
db.init_app(app)

# 데이터베이스 초기화 여부를 추적하는 플래그
db_initialized = False

@app.before_request
def initialize_db():
    global db_initialized
    if not db_initialized:
        db.create_all()
        db_initialized = True

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['name']
        preferred_category = request.form['preferred_category']
        
        if User.query.filter_by(UserID=user_id).first():
            return 'ID already exists!'

        new_user = User(UserID=user_id, Name=name, PreferredCategory=preferred_category)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        user = User.query.filter_by(UserID=user_id).first()
        
        if user is None:
            return 'Invalid ID!'
        
        session['user_id'] = user.UserID
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.as_dict() for restaurant in restaurants])

@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    data = request.json
    new_restaurant = Restaurant(
        Name=data['Name'],
        Location=data['Location'],
        OpeningHours=data['OpeningHours'],
        ContactInfo=data['ContactInfo']
    )
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify(new_restaurant.as_dict()), 201

@app.route('/delete_restaurant/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant deleted successfully'}), 200

# Helper function to convert SQLAlchemy model instance to dictionary
def as_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

# Add this method to each model
Restaurant.as_dict = as_dict
Menu.as_dict = as_dict
User.as_dict = as_dict
Review.as_dict = as_dict
TodayMenu.as_dict = as_dict

if __name__ == '__main__':
    app.run(debug=True)
