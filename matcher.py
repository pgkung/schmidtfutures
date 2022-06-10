from collections import defaultdict, deque

class Match(object):
	def __init__(self, user, opportunity):
		self.user = user
		self.opportunity = opportunity

# This class runs the matching algorithm and contains data to access said matches and unmatched users/opportunities as well
# The matching algorithm relies on the opportunities not having a ranked preference for the user. This way, the first person to apply
# will never be evicted. With this assumption the matcher sorts the users and opportunities by the least amount posted to avoid the possibility
# of an opportunity being left open that could've been filled as the second choice for a user currently at their first choice. 

# Note: with more time storing matches in a database would've been nice, but I think working in memory is good enough for now
class Matcher(object):
	def __init__(self):
		self.users = []
		self.opportunities = []
		self._reset_match_vars()

	def _reset_match_vars(self):
		self.role_to_opportunity = defaultdict(list)
		self.unmatched_users = None
		self.unmatched_opportunities = None
		self.match_by_user = {}
		self.match_by_opportunity = defaultdict(list)
		self.matches = []

	def _generate_role_to_opportunity(self):
		for opportunity in self.opportunities:
			for role in opportunity.roles:
				self.role_to_opportunity[role].append(opportunity)

	def _attempt_to_match_user(self, user):
		for role in user.interested_in:
			opportunities = self.role_to_opportunity[role]
			if not opportunities:
				continue
			# sort so we match unmatched first and hit the ones with less chance of being filled. Sort everytime since num matches may have changed
			opportunities.sort(key=lambda opportunity: (len(self.match_by_opportunity[opportunity.id_]), opportunity.roles))
			# Assumes roles only have headcount of 1
			opportunity = opportunities.pop(0)
			match = Match(user, opportunity)
			self.match_by_user[user.id_] = match
			self.match_by_opportunity[opportunity.id_].append(match)
			# Users can only have one match so we don't have to loop through everything
			return

	def _calculate_unmatched_users(self):
		self.unmatched_users = [user for user in self.users if user.id_ not in self.match_by_user.keys()]

	def _calculate_unmatched_opportunities(self):
		self.unmatched_opportunities = [opp for opp in self.opportunities if opp.id_ not in self.match_by_opportunity.keys()]


	# Generates suggested matches by iterating through sorted users and opportunities. This will be 
	# user biased since SF bets on people. Assumes interests are listed in order of preference. Prioritizes
	# users with less preferences and opportunities with less roles to ensure there are no instances where 
	# a potential match ends up missed. This unintentionally penalizes people/orgs that list more roles though
	def match(self, users, opportunities):
		self._reset_match_vars()
		self.users = sorted(users, key=lambda user: len(user.interested_in))
		self.opportunities = opportunities
		self._generate_role_to_opportunity()
		users_to_match = deque(self.users)
		while users_to_match:
			user = users_to_match.popleft()
			self._attempt_to_match_user(user)
		self.matches = list(self.match_by_user.values())
		return self.matches

	def get_matches(self):
		return self.matches

	def get_matches_by_user(self):
		return self.matches

	def get_matches_by_opportunities(self):
		return list(self.match_by_opportunity.values())

	def get_match_for_user(self, user_id):
		return self.match_by_user[user_id]

	def get_matches_for_opportunity(self, opportunity_id):
		return self.match_by_opportunity[opportunity_id]

	def get_unmatched_users(self):
		if not self.unmatched_users:
			self._calculate_unmatched_users()
		return self.unmatched_users
		
	def get_unmatched_opportunities(self):
		if not self.unmatched_opportunities:
			self._calculate_unmatched_opportunities()
		return self.unmatched_opportunities
