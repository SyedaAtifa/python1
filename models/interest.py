from extensions import db

class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    advices = db.relationship('Advice', backref='interest', lazy=True)

    def __repr__(self):
        return f"<Interest {self.name}>"
