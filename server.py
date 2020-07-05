from flask import Flask, request
from flask_api import status
#from OpenSSL import SSL

import json
import uuid

from conf.config import SERVER_IP, SERVER_PORT
from middleware.auth import AuthMiddleware
from model.user_profile import UserProfile

import helper.error as error
import helper.db as db_helper
import helper.session as session

app = Flask('Flask-Authentication')

#context = SSL.Context(SSL.SSLv23_METHOD)

def register_middleware():
	app.wsgi_app = AuthMiddleware(app.wsgi_app)

register_middleware()

#----------------------------------------------------------------------------------
@app.route('/user/signup', methods=['POST'])
def user_signup():
	json_data = request.get_json()
	print('json_data:', json_data)
	if json_data is None:
		return 'Bad Request', status.HTTP_400_BAD_REQUEST

	# Validate User Data
	if json_data.get('email_id') is None:
		return 'Missing field: email_id', status.HTTP_400_BAD_REQUEST

	if json_data.get('name') is None:
		return 'Missing field: name', status.HTTP_400_BAD_REQUEST

	if json_data.get('password') is None:
		return 'Missing field: password', status.HTTP_400_BAD_REQUEST

	# TODO: Adding warning if unwanted data is supplied in the request

	user_profile = UserProfile(**{
			'email_id': json_data['email_id'],
			'name': json_data['name'],
			'password': json_data['password']
		}
	)

	try:
		# Save User Data in DB
		user_profile = db_helper.save_user_profile(user_profile)
		return user_profile.to_json()
	except error.UserExists:
		return 'User already exists', status.HTTP_400_BAD_REQUEST
	except Exception as e:
		print('error:', e)
		return '', status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/user/login', methods=['POST'])
def user_login():
	email_id = request.authorization.get('username')
	password = request.authorization.get('password')

	if not email_id:
		return 'Missing Field: username in Basic Authentication', status.HTTP_400_BAD_REQUEST

	if not password:
		return 'Missing Field: password in Basic Authentication', status.HTTP_400_BAD_REQUEST

	try:
		if not db_helper.verify_username_password(email_id, password):
			return 'Authentication Failed', status.HTTP_401_UNAUTHORIZED
	except error.UserNotFound as e:
		return 'User not found', status.HTTP_400_BAD_REQUEST
	except Exception as e:
		print('user_login.e', e)
		return '', status.HTTP_500_INTERNAL_SERVER_ERROR

	try:
		access_token = session.create_user_session(email_id)
		return {
			'access_token': access_token
		}
	except Exception as e:
		print('user_login.create_user_session.e', e)
		return '', status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/user/profile', methods=['GET'])
def user_profile():
	session_id = request.environ.get('SESSION_ID')
	if not session_id:
		return {
			'Access denied'
		}, status.HTTP_401_UNAUTHORIZED

	try:
		user_profile = db_helper.get_user_profile_from_session_id(session_id)
		return user_profile
	except error.SessionNotFound as e:
		return 'Access denied', status.HTTP_400_BAD_REQUEST
	except Exception as e:
		return '', status.HTTP_500_INTERNAL_SERVER_ERROR

if __name__ == "__main__":
	app.run(host=SERVER_IP, port=SERVER_PORT, debug=True, threaded=True, ssl_context=None)
