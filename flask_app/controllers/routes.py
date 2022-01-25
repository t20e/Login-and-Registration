# email check needs to be done 

from flask import render_template, redirect, request, session
import flask
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logged_in')
def logged_in():
    if 'id' not in session:
        flash('please log in')
        return redirect('/')
    return render_template('logged_in.html')

@app.route('/create_user', methods=['POST'])
def add_user():
    session.clear()
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : request.form['password'],
        'email' : request.form['email'],
        'password2' : request.form['password'],
        'password_confirm2' : request.form['password_confirm']
    }
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']
    if not User.check_registration_fields(data):
        print('red fl6ags')
    else:
        return redirect('/')
    holder = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = holder
    create = User.create_user(data)
    return redirect('/logged_in')


@app.route('/login', methods=['POST'])
def loggin_in():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password'],
    }
    holder = User.check_password_email_login(data) 
    if not holder:
        flash("invalid password/email")
        return redirect('/')
    if not bcrypt.check_password_hash(holder.password, request.form['password']):
        flash('invalid password/email')
        return redirect('/')
    session['first_name'] = holder.first_name
    session['last_name'] = holder.last_name
    session['email'] = holder.email
    session['id'] = holder.id
    return redirect('/logged_in')
            
@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')


