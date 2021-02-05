from app import db

class TestModel(db.Model):
    __tablename__ = 'mmm'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, default=1)
    m0 = db.Column(db.String(100), nullable=False)
    m0g = db.Column(db.String(100), nullable=False)
    m1 = db.Column(db.String(100), nullable=False)
    m1g = db.Column(db.String(100), nullable=False)
    m2 = db.Column(db.String(100), nullable=False)
    m2g = db.Column(db.String(100), nullable=False)
