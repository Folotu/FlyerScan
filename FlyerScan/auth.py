from flask import Flask, request, redirect, url_for, flash, Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google
from flask import jsonify
from .models import *

auth = Blueprint('auth', __name__)

# Route to handle login
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if len(current_user.roles) == 2:
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('views.index'))
                
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('auth.login'))

    elif request.method == 'GET':
        return render_template("login.html",user=current_user, )
    
@auth.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    account_info = google.get('/oauth2/v2/userinfo')
    if account_info.ok:
        account_info_json = account_info.json()
        email = account_info_json['email']
        username = account_info_json['given_name']

        if email is not None and account_info_json['verified_email'] is True:
 
            user = Users.query.filter_by(email=email).first()
            if user:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if len(current_user.roles) == 2:
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('views.index'))
            else:
                new_user = Users(email=email, username=username, roles = [Role.query.first()])
                db.session.add(new_user)

                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.index'))

        else:
            return jsonify({'status': 'Something went wrong While trying to sign in with your google account.'})

    return jsonify({'status': 'failed'})
    
# @auth.route('/login/github')
@auth.route('github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    
    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        email = account_info_json['email']
        username = account_info_json['login']

        if email is not None:
 
            user = Users.query.filter_by(email=email).first()
            if user:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if len(current_user.roles) == 2:
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('views.index'))
            else:
                new_user = Users(email=email, username=username, roles = [Role.query.first()])
                db.session.add(new_user)

                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.index'))
        else:
            gitUserId = account_info_json['id']
            gitEmailConcat = f'{gitUserId}@githubForFlyerScan.com'

            user = Users.query.filter_by(email=gitEmailConcat).first()
            if user:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                if len(current_user.roles) == 2:
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('views.index'))
            else:
                userRole = Role.query.first()
                new_user = Users(email=gitEmailConcat, username=username, roles = [userRole])
                db.session.add(new_user)
            
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.index'))


# Route to logout
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Log out successfull!', category='success')
  return redirect(url_for('auth.login'))


# Route to handle signup
@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Users(email=email, username=username, password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)

            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.index'))


    return render_template("sign_up.html", user=current_user)