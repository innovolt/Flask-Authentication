from werkzeug.wrappers import Request, Response, ResponseStream
from flask_api import status
import helper.session as session

class AuthMiddleware():
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		request = Request(environ)

		# Get the Session ID from Bearer Token
		auth = request.headers.get('Authorization')
		if auth:
			(token_type, token) = auth.split()
			if token_type == 'Bearer':
				session_id = session.get_session_id(token)
				print('session_id', session_id)
				if session_id is None:
					res = Response(u'Authorization failed', mimetype='text/plain', status=status.HTTP_401_UNAUTHORIZED)
					return res(environ, start_response)
				environ['SESSION_ID'] = session_id
				return self.app(environ, start_response)
			elif token_type == 'Basic':
				return self.app(environ, start_response)
			else: # Unhandled auth hdr
				res = Response(u'Bad Request', mimetype='text/plain', status=status.HTTP_400_BAD_REQUEST)
				return res(environ, start_response)
		else:
			return self.app(environ, start_response)
