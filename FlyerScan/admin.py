from flask import Flask 
from flask_admin import Admin, AdminIndexView, expose
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user, UserMixin
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, login_required, current_user
from . import db, app
import json
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

from .models import Users, Role # Category, Post, Comment, Reply, Upvote

class Administrator(ModelView):
	@login_required
	def is_accessible(self):
		return super().is_accessible()

	column_display_pk = True
	column_hide_backrefs = False
	column_list = []


class MyAdminView(AdminIndexView):
	def is_accessible(self):
		print(current_user)
		return (current_user.is_active and
				current_user.is_authenticated and
				current_user.has_roles('superuser')
		)
	@expose('/')
	def index(self):
		arg1 = 'Hello'
		return self.render('adminhome.html', arg1=arg1)


user_datastore = SQLAlchemyUserDatastore(db)


def appnamey(Daname):
	admin = Admin(Daname, name='Admin', template_mode='bootstrap3', index_view=MyAdminView()) 

	admin.add_view(Administrator(Users, db.session))
	admin.add_view(Administrator(Role, db.session))
# 	admin.add_view(Administrator(Category, db.session))
# 	admin.add_view(Administrator(Post, db.session))
# 	admin.add_view(Administrator(Comment, db.session))
# 	admin.add_view(Administrator(Reply, db.session))
# 	admin.add_view(Administrator(Upvote, db.session))



def superuserNewDB(Daname):
	with Daname.app_context():
		user_role = Role(name='user')
		super_user_role = Role(name='superuser')
		db.session.add(user_role)
		db.session.add(super_user_role)
		db.session.commit()
	
		test_user = user_datastore.create_user(
			username='Admin',
			email='admin@admin.com',
			password = generate_password_hash('admin', method='sha256'),)
			# roles=[user_role, super_user_role]
			# )
		db.session.commit()