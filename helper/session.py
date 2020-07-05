import base64
import hashlib
import secrets

import helper.db as db_helper

# 16 bytes
BEARER_TOKEN_LENGTH = 16 

def generate_bearer_token():
	#return "abcdef123456789abcdef"
	return secrets.token_hex(BEARER_TOKEN_LENGTH)

def get_session_id(bearer_token):
	return hashlib.sha256(bearer_token.encode()).hexdigest()

def create_user_session(email_id):
	bearer_token = generate_bearer_token()
	session_id = get_session_id(bearer_token)
	
	try:
		_ = db_helper.save_session(session_id, email_id)
		return bearer_token
	except Exception as e:
		raise e
