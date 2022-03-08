from app import db


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(60))
    data = db.Column(db.LargeBinary)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
    