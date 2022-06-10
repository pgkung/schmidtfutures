class Opportunity(object):
	def __init__(self, id, organization, roles, email):
		self.id_ = id
		self.organization = organization
		self.roles = [] if not roles else roles
		self.email = email