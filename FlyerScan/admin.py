from flask import Flask 
from flask_admin import Admin, AdminIndexView, expose
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, login_required, current_user
from . import db
import json
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

from .models import Users, Role, ScanHistory

class Administrator(ModelView):
	
	def is_accessible(self):
		if (current_user.is_active and
			current_user.is_authenticated and
			current_user.has_roles('superuser')):

			column_display_pk = True
			column_hide_backrefs = False
			
			column_list = []
			return super().is_accessible()
	
	def inaccessible_callback(self, name, **kwargs):
		if not self.is_accessible():
			return redirect(url_for('auth.login'))	

class MyAdminView(AdminIndexView):
	@login_required
	def is_accessible(self):
		if (current_user.is_active and
			current_user.is_authenticated and
			current_user.has_roles('superuser')):

			return super().is_accessible()

	@expose('/')
	@login_required
	def index(self):
		arg1 = f'<{current_user.username}>'
		return self.render('adminhome.html', arg1=arg1, )

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)

def appnamey(Daname):
	admin = Admin(Daname, name='Admin', template_mode='bootstrap3', index_view=MyAdminView()) 
	listOfModels = [Users, Role, ScanHistory]

	AllColList = []
	for i in range(len(listOfModels)):
		AllColList.append([c_attr.key for c_attr in inspect(listOfModels[i]).mapper.column_attrs])

	for j in range(len(AllColList)):
		daSesh = db.session
		tempAdmin = Administrator(listOfModels[j], daSesh)

		tempAdmin.column_list = AllColList[j]

		admin.add_view(tempAdmin)


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
			password = generate_password_hash('admin', method='sha256'),
			roles=[user_role, super_user_role]
			)
		db.session.commit()