import helper.error as error
import sqlite3

def cleanup(db_conn=None, cursor_conn=None):
	try:
		if cursor_conn is not None:
			cursor_conn.close()
		
		if db_conn is not None:
			db_conn.close()
	except Exception as e:
		raise e

def get_db_connection():
	db_conn = None
	try:
		db_conn = sqlite3.connect("test.db")
		return db_conn
	except Exception as e:
		raise e

def run_select_query(query):
	print('query:', query)
	db_conn = cursor_conn = None
	try:
		db_conn = get_db_connection()
		cursor_conn = db_conn.cursor()
		cursor_conn.execute(query)
		return cursor_conn.fetchall()
	except Exception as e:
		raise e
	finally:
		cleanup(db_conn, cursor_conn)

def run_insert_query(query):
	print('query:', query)
	db_conn = cursor_conn = None
	try:
		db_conn = get_db_connection()
		cursor_conn = db_conn.cursor()
		cursor_conn.execute(query)
		db_conn.commit()
	except Exception as e:
		raise e
	finally:
		cleanup(db_conn, cursor_conn)

def get_user_profile(email_id=None, user_id=None):
	where_query_str = ''
	if email_id is not None:
		where_query_str += ('email_id="%s"' % email_id)

	if user_id is not None:
		where_query_str += (' AND ' if where_query_str else '')
		where_query_str += ('user_id="%s"' % user_id)

	if where_query_str:
		where_query_str = 'where ' + where_query_str

	query = 'select * from user %s' % where_query_str
	try:
		user_profile = run_select_query(query)

		if not user_profile:
			raise error.UserNotFound()

		if len(user_profile) > 1:
			raise error.DuplicateUsersFound()

		return user_profile[0]
	except Exception as e:
		raise e

def save_user_profile(user_profile):
	'''
		Arg: user_profile of type model.user_profile.UserProfile
		The purpose is to validate if this user already exists. If yes then return
		error UserExists otherwise add it to DB
	'''
	try:
		_ = get_user_profile(user_profile.email_id)
		raise error.UserExists
	except error.UserNotFound as e:
		print('error.UserNotFound')
		try:
			query = 'insert into user (email_id, user_id, name, password) values ("%s", "%s", "%s", "%s")' % (user_profile.email_id, user_profile.user_id, user_profile.name, user_profile.password)
			_ = run_insert_query(query)
			return user_profile
		except Exception as e:
			print('error.UserNotFound.e:', e)
			raise e
	except Exception as e:
		print('save_user_profile.e:', e)
		raise e

def save_session(session_id, email_id):
	try:
		query = 'insert into session (session_id, email_id) values ("%s", "%s")' % (session_id, email_id)
		_ = run_insert_query(query)
		return ""
	except Exception as e:
		print('save_session.e:', e)
		raise e

def verify_username_password(email_id, password):
	try:
		user_profile = get_user_profile(email_id=email_id)
		return password == user_profile[-1]
	except Exception as e:
		raise e

def get_email_id_from_session_id(session_id):
	try:
		query = 'select email_id from session where session_id="%s"' % session_id
		records = run_select_query(query)
		print('get_user_profile_from_session_id.records:', records)
		if not records:
			raise error.SessionNotFound()
		return records[0][0]
	except Exception as e:
		print('get_email_id_from_session_id.e:', e)
		raise e

def get_user_profile_from_session_id(session_id):
	try:
		email_id = get_email_id_from_session_id(session_id)
		user_profile = get_user_profile(email_id=email_id)
		return {
			'email_id': user_profile[0],
			'user_id': user_profile[1],
			'name': user_profile[2]
		}
	except Exception as e:
		print('get_user_profile_from_session_id.e:', e)
		raise e