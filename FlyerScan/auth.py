from flask import Flask, request, redirect, url_for, flash, Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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
                if current_user.roles[0].name == 'superuser':
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


# Route to logout
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Log out successfull!', category='success')
  return redirect(url_for('auth.login'))