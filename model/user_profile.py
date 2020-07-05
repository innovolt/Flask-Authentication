import uuid

class UserProfile(object):
	def __init__(self, email_id=None, name=None, password=None):
		self.user_id = uuid.uuid4()
		print('user_id:', self.user_id)
		self.email_id = email_id
		self.name = name
		self.password = password

	def get_user_id(self):
		return str(self.user_id)

	def to_json(self):
		return {
			'user_id': self.user_id,
			'email_id': self.email_id,
			'name': self.name
		}
