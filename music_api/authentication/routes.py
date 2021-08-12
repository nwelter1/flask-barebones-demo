from flask import Blueprint, render_template, request, redirect, url_for, flash
from music_api.forms import UserLoginForm
from music_api.models import db, User, check_password_hash
from flask_login import login_user, logout_user, login_required
from music_api import mail
from flask_mail import Message

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()
        #Sending Auto-Email
        msg = Message("Welcome!", recipients=[email])
        msg.body = f"Drones are the shit {email} ! Keep reppin drones til the day you die here is your pw: {password}!"
        mail.send(msg)
        flash(f'You have created an account for {email}', 'create-success')
        return redirect(url_for('auth.signin'))

    return render_template('signup.html', form = form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash(f'Successfully logged in as: {email}', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash('Incorrect emal/password. Please try again.', 'auth-fail')
            return redirect(url_for('auth.signin'))


    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Successfully logged out', 'auth-success')
    return redirect(url_for('site.home'))