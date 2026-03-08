from extensions import db

class Advice(db.Model):
    __tablename__ = 'advice'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), nullable=False)
    rating_sum = db.Column(db.Integer, default=0)
    rating_count = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # optional reference to a user

    def average_rating(self):
        return self.rating_sum / self.rating_count if self.rating_count else None

    def __repr__(self):
        return f"<Advice {self.id} for interest {self.interest_id}>"
