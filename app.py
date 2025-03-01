from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime,timezone


app = Flask(__name__)
app.secret_key = '40bbd49979fc705cf10e7231ab227d33'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Studyrooms(db.Model):
    room_id = db.Column(db.Integer,primary_key=True)
    room_name = db.Column(db.String(100),nullable=False)
    room_code = db.Column(db.String(20),nullable=False,unique=True)
    owner_id = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))

class Roommembers(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    joined_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return "Passwords do not match!"

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return f"Database error: {e}"
        
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('homepage'))
        else:
            return "Invalid email or password!"

    return render_template('signin.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html')

@app.route('/community')
def community():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template('community.html')

@app.route('/solo-study')
def solo_study():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template('solo-study.html')

@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template('homepage.html', user_name=session['user_name'])

@app.route('/createstudyroom', methods=['GET', 'POST'])
def createstudyroom():
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        room_code = request.form.get('room_code')

        if not room_name or not room_code:
            flash("Please fill in all fields", "error")
            return render_template('createstudyroom.html')

        # Check if room_code already exists
        existing_room = Studyrooms.query.filter_by(room_code=room_code).first()
        if existing_room:
            flash("Unique Code already exists. Try another one.", "error")
            return render_template('createstudyroom.html')

        # Get logged-in user as owner_id
        owner_id = session.get('user_id')
        if not owner_id:
            flash("You need to be logged in to create a study room.", "error")
            return redirect(url_for('signin'))

        new_room = Studyrooms(room_name=room_name, room_code=room_code, owner_id=owner_id)
        db.session.add(new_room)
        db.session.commit()

        flash("Study Room created successfully!", "success")
        return redirect(url_for('studyroom'))

    return render_template('createstudyroom.html')


@app.route('/studyroom',methods=['GET','POST'])
def studyroom():
    return render_template('studyroom.html')

@app.route('/joinstudyroom',methods=['GET','POST'])
def joinstudyroom():
    return render_template('joinstudyroom.html')

if __name__ == '__main__':
    app.run(debug=True)
