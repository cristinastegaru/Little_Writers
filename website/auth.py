from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def log_in():
    message = ''
    if request.method == 'POST':
        username = request.form.get('Uname')
        password = request.form.get('Pass')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                message = 'Incorrect password'
        else:
            message = "Username doesn't exist"

    return render_template("log_in.html", text= message, user=current_user)

@auth.route('/logout')
def logout():
    return "<h1>Log Out</h1>"

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    message = ''
    if request.method == 'POST':
        email = request.form.get('Email')
        name = request.form.get('Name')
        username = request.form.get('Uname')
        password = request.form.get('Pass')
        password2 = request.form.get('Pass2')
        user = User.query.filter_by(username=username).first()
        if user:
            message= "This username already exists!"
        else:
            user = User.query.filter_by(email=email).first()
            if user: 
                message= "Email already linked to an account!"
            else:
                if len(name) > 0:
                    if len(email) > 0:
                        if len(username) > 0:
                            if len(password) > 5:
                                if password != password2:
                                    message = "Passwords don't match"
                                else:
                                    message = "Account created succesfully!"
                                    user = User(email=email, name=name, username=username, password=generate_password_hash(password, method='sha256'))
                                    db.session.add(user)
                                    db.session.commit()
                                    login_user(user,remember=True)
                                    return redirect(url_for('views.home'))
                            else:
                                message = "Password needs to be longer!"
                        else:
                            message = "Please introduce a username!"
                    else:
                        message = "Please introduce your email!"
                else:
                    message = "Please introuduce your name!"

    return render_template("sign_up.html",text=message) 