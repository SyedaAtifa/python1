import json
from extensions import db
from models.interest import Interest
from models.advice import Advice

class CareerAdvice:
    @staticmethod
    def generate(interest_name):
        # try to find advice entries in the database first
        interest = Interest.query.filter_by(name=interest_name).first()
        if interest:
            advices = Advice.query.filter_by(interest_id=interest.id).all()
            if advices:
                # pick the highest-rated advice
                advices.sort(key=lambda a: a.average_rating() or 0, reverse=True)
                return advices[0], advices
        # otherwise fall back to a JSON file that contains default mappings
        try:
            with open('advice_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                text = data.get(interest_name)
                if text:
                    return text, []
        except FileNotFoundError:
            pass
        return "Please select a valid interest area.", []
