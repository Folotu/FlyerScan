from flask import Blueprint, render_template, request, flash, jsonify, abort, redirect, url_for
from flask_login import login_required, current_user
from . import db, app
import json
from .models import *
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def index():

        if (current_user.is_anonymous):
            person = "Guest"
            return render_template('landing.html', person=person,)    
        
        else:
            person = current_user.username
        return render_template('index.html', person=person)