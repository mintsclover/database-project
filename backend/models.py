from database import db

class Restaurant(db.Model):
    RestaurantID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Location = db.Column(db.String(255), nullable=False)
    OpeningHours = db.Column(db.String(100))
    ContactInfo = db.Column(db.String(100))

class Menu(db.Model):
    MenuID = db.Column(db.Integer, primary_key=True)
    RestaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.RestaurantID'), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Category = db.Column(db.String(50))
    Description = db.Column(db.Text)
    ImageURL = db.Column(db.String(255))

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    PreferredCategory = db.Column(db.String(50))

class Review(db.Model):
    ReviewID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    MenuID = db.Column(db.Integer, db.ForeignKey('menu.MenuID'), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    ReviewText = db.Column(db.Text)
    ReviewDate = db.Column(db.Date)

class TodayMenu(db.Model):
    MenuID = db.Column(db.Integer, db.ForeignKey('menu.MenuID'), primary_key=True)
    Date = db.Column(db.Date, primary_key=True)
    RecommendationReason = db.Column(db.Text)
