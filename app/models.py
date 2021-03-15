from app import db

class User(db.Model):
    tid = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.String(10), unique=True)
    b = db.Column(db.String(255))
    
    def __repr__(self):
        return '<User {},{}>'.format(self.id, self.tid)  