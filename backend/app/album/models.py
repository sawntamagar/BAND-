from app import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(30), nullable=False)
    songs = db.relationship('UploadSong', backref='album',cascade="all,delete", lazy=True)
    
    def update(self, album_name):
        self.album_name = album_name
        db.session.commit()
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
        
class UploadSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(60))
    data = db.Column(db.LargeBinary)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)    
        db.session.commit()
    