from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    PreferredCategory = db.Column(db.String(50))

class Restaurant(db.Model):
    RestaurantID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Location = db.Column(db.String(100))
    OpeningHours = db.Column(db.String(100))
    ContactInfo = db.Column(db.String(100))

class Menu(db.Model):
    MenuID = db.Column(db.Integer, primary_key=True)
    RestaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.RestaurantID'))
    ItemName = db.Column(db.String(100))
    Price = db.Column(db.Float)
    Category = db.Column(db.String(50))

class Review(db.Model):
    ReviewID = db.Column(db.Integer, primary_key=True)
    RestaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.RestaurantID'))
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    Rating = db.Column(db.Integer)
    Comment = db.Column(db.String(500))

class TodayMenu(db.Model):
    TodayMenuID = db.Column(db.Integer, primary_key=True)
    RestaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.RestaurantID'))
    Date = db.Column(db.Date)
    MenuID = db.Column(db.Integer, db.ForeignKey('menu.MenuID'))
