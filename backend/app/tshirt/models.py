from datetime import datetime
from app import db

    
class Customer(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    name =  db.Column(db.String(500), nullable = False, unique=False) 
    email =  db.Column(db.String(500), nullable = False)
    location =  db.Column(db.String(500), nullable = False) 
    phone_number = db.Column(db.String(20), nullable = False)
    orders = db.relationship("Order", backref="customer", cascade="all,delete", lazy='dynamic')
    
    def __init__(self, name, location, phone_number, email):
        self.name = name
        self.location = location
        self.phone_number = phone_number
        self.email = email
      

    def __repr__(self):
        return '<name %r>' % self.id
       
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
            
    def update(self, name, location, phone_number):
        self.name=name
        self.location=location
        self.phone_number=phone_number
        db.session.commit()
        
    def save(self):
        db.session.add(self)
        db.session.commit()        
        
    
class Order(db.Model):
    
    id = db.Column('order_id', db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    quantity = db.Column(db.String(500), nullable = False)
    created_at = datetime.now()
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
     
    def __init__(self, size, quantity, customer_id):
        self.size = size
        self.quantity = quantity
        self.customer_id = customer_id
    
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
          
    def update(self, size, quantity):
        self.size=size
        self.quantity=quantity
       
        db.session.commit()
        
    def save(self):
        db.session.add(self)
        db.session.commit()        
        