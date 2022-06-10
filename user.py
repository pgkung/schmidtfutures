class User(object):
	def __init__(self, id, first_name, last_name, email, interested_in):
		self.id_ = id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.interested_in = [] if not interested_in else interested_in
