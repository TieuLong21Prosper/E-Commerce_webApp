from datetime import datetime
from shop import db

class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique = True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #define relationship to other classes
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id') ,nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id') ,nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    #define var images of form fields
    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')
    #define toString method
    def __repr__(self):
        return '<AddProduct %r>' % self.name

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique = True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique = True)

