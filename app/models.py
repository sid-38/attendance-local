from app import db

class User(db.Model):
    tid = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.String(10), unique=True)
    b = db.Column(db.String(255))
    
    def __repr__(self):
        return '<User {},{}>'.format(self.id, self.tid)

class Rollcall(db.Model):
    __tablename__ = 'rollcall'

    id = db.Column(db.String(10), unique=True)
    date = db.Column(db.String(12), unique=True)
    time = db.Column(db.String(12))

    __table_args__ = ( 
            db.PrimaryKeyConstraint(id,date,
                ),
            )

    def __repr__(self):
        return '<Rollcall {},{},{}>'.format(self.date,self.id,self.time)
