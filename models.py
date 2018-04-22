from app import db
import datetime
from sqlalchemy import inspect

def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs}

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	name = db.Column(db.String(120), nullable=True)
	token = db.Column(db.Text, nullable=True)
	refresh_token = db.Column(db.Text, nullable=True)
	token_uri = db.Column(db.Text, nullable=True)
	client_id = db.Column(db.Text, nullable=True)
	client_secret = db.Column(db.Text, nullable=True)
	scopes = db.Column(db.Text, nullable=True)
	emails = db.relationship('Email', backref='user', lazy=True)


class Email(db.Model):
	__tablename__ = 'email'

	id = db.Column(db.Integer, primary_key=True)
	message_id = db.Column(db.Text, nullable=False)
	sender_email = db.Column(db.String(120), nullable=False)
	body = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
