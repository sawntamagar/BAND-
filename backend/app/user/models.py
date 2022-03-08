from werkzeug.security import generate_password_hash
from flask_login import UserMixin, login_manager
from app import db
from app.file.models import Upload


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    active = db.Column('is_active', db.Boolean(), nullable = False, server_default = '1')
    username = db.Column(db.String(255), nullable = False, unique = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255))
    uploads = db.relationship('Upload', backref='user', lazy=True)
    
    

    def __repr__(self):
        return f"<user {self.username}>"
        
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
            
    def update(self, username, email):
        self.username=username
        self.email=email
       
        db.session.commit()
        
    def save(self):
        db.session.add(self)
        db.session.commit()        
        
        
