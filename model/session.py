class Session(object):
	# After 5 minutes, session is expired
	expiry_time = 300

	def __init__(self):
		self.session_id = None
		self.expiry_time = None
		self.user_id = None

	def set_session_id(self, session_id):
		self.session_id = session_id

	def set_expiry_time(self, expiry_time):
		self.expiry_time = expiry_time

	def set_user_id(self, user_id):
		self.user_id = user_id
