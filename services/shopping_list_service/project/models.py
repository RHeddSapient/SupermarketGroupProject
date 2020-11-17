from project.main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import expression


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), unique = True, nullable=False)

    def __repr__(self):
        return self.username

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name =  db.Column(db.String(20), nullable=True)
    x_size =  db.Column(db.Integer, nullable=False)
    y_size =  db.Column(db.Integer, nullable=False)
    store_map = db.Column(JSON)

    def __repr__(self):
        return self.id

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False  )
    title =  db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return self.id

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_name =  db.Column(db.String(20), unique= True, nullable=False)
    prod_category = db.Column(db.String(20), nullable=False) 
    stocked = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    def __repr__(self):
        return self.id

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'),nullable=False )
    x_loc=  db.Column(db.Integer)
    y_loc=  db.Column(db.Integer)

    def __repr__(self):
        return self.id

class ListProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False )
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False )

    def __repr__(self):
        return self.id
