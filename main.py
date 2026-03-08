import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from extensions import db, login_manager
from forms import RegistrationForm, LoginForm, AdviceForm, InterestForm, RatingForm
from flask_wtf import CSRFProtect
from models.user import User
from models.interest import Interest
from models.advice import Advice
from models.career_advice import CareerAdvice
from flask_login import login_user, logout_user, login_required, current_user

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Use /tmp for Vercel serverless, local for development
if os.environ.get('VERCEL'):
    db_path = '/tmp/career.db'
else:
    db_path = os.path.join(BASE_DIR, 'instance/career.db')

# Ensure instance directory exists locally
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
# CSRF protection for all forms
csrf = CSRFProtect(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring"""
    return jsonify({'status': 'ok', 'message': 'Career Advice Boat is running'}), 200

def create_tables():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")
        return
    
    # seed default interests and advice from JSON file
    try:
        import json
        with open('advice_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for interest_name, advice_text in data.items():
                try:
                    interest = Interest.query.filter_by(name=interest_name).first()
                    if not interest:
                        interest = Interest(name=interest_name)
                        db.session.add(interest)
                        db.session.flush()  # get id
                    # check if advice already exists
                    existing = Advice.query.filter_by(interest_id=interest.id, text=advice_text).first()
                    if not existing:
                        db.session.add(Advice(interest_id=interest.id, text=advice_text))
                except Exception as e:
                    print(f"Error seeding {interest_name}: {e}")
                    db.session.rollback()
            db.session.commit()
    except FileNotFoundError:
        print("advice_data.json not found, skipping seed")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.session.rollback()

@app.route('/')
def index():
    interests = Interest.query.order_by(Interest.name).all()
    return render_template('index.html', interests=interests)

@app.route('/response', methods=['POST'])
def response():
    name = request.form.get('name')
    interest = request.form.get('interest')

    advice_obj, advices_list = CareerAdvice.generate(interest)
    # advice_obj may be the first Advice instance or raw text
    if isinstance(advice_obj, Advice):
        advice_text = advice_obj.text
        advice_id = advice_obj.id
    else:
        advice_text = advice_obj
        advice_id = None

    return render_template('response.html', name=name, advice=advice_text, advice_id=advice_id, other=advices_list)

@app.route('/api/advice', methods=['POST'])
def api_advice():
    data = request.get_json() or {}
    interest = data.get('interest')
    advice_obj, _ = CareerAdvice.generate(interest)
    if isinstance(advice_obj, Advice):
        return jsonify({'advice': advice_obj.text, 'id': advice_obj.id})
    else:
        return jsonify({'advice': advice_obj})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_interest', methods=['GET', 'POST'])
@login_required
def add_interest():
    form = InterestForm()
    if form.validate_on_submit():
        name = form.name.data.strip().lower()
        if Interest.query.filter_by(name=name).first():
            flash('Interest already exists.', 'warning')
        else:
            db.session.add(Interest(name=name))
            db.session.commit()
            flash('Interest added.', 'success')
        return redirect(url_for('index'))
    return render_template('add_interest.html', form=form)

@app.route('/submit_advice', methods=['GET', 'POST'])
@login_required
def submit_advice():
    form = AdviceForm()
    # populate choice list
    form.interest.choices = [(i.name, i.name.title()) for i in Interest.query.order_by(Interest.name).all()]
    if form.validate_on_submit():
        interest = Interest.query.filter_by(name=form.interest.data).first()
        if interest:
            advice = Advice(text=form.text.data, interest_id=interest.id, created_by=current_user.id)
            db.session.add(advice)
            db.session.commit()
            flash('Advice submitted. Thank you!', 'success')
            return redirect(url_for('index'))
    return render_template('submit_advice.html', form=form)

@app.route('/rate', methods=['POST'])
def rate():
    form = RatingForm()
    if form.validate_on_submit():
        advice = Advice.query.get(form.advice_id.data)
        if advice:
            advice.rating_sum += form.rating.data
            advice.rating_count += 1
            db.session.commit()
            flash('Thanks for your rating!', 'success')
            return redirect(url_for('index'))
    flash('Failed to submit rating.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # create database and seed data before first request
    with app.app_context():
        create_tables()
    app.run(debug=True)
