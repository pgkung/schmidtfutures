import unittest
from user import User
from opportunity import Opportunity
from matcher import Matcher



class MatcherTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.matcher = Matcher()

	def test_it_returns_empty_before_matching(self):
		matcher = Matcher()

		assert len(matcher.get_unmatched_users()) == 0
		assert len(matcher.get_unmatched_opportunities()) == 0

	def test_it_returns_unmatched(self):
		users = [User(1, "Peter", "Kung", "test@gmail.com", None)]
		opportunities = [Opportunity(1, "Schmidt Futures", None, "sf@schmidtfutures.com")]

		matches = self.matcher.match(users, opportunities)

		self.assertEquals(self.matcher.get_unmatched_opportunities(), opportunities)
		self.assertEquals(self.matcher.get_unmatched_users(), users)

	def test_it_matches(self):
		users = [User(1, "Peter", "Kung", "test@gmail.com", ["Software Engineer"])]
		opportunities = [Opportunity(1, "Schmidt Futures", ["Software Engineer"], "sf@schmidtfutures.com")]

		matches = self.matcher.match(users, opportunities)

		assert len(matches) == 1
		assert matches[0].user == users[0]
		assert matches[0].opportunity == opportunities[0]

	def test_it_matches_as_many_as_possible(self):
		users = [User(1, "Peter", "Kung", "test@gmail.com", ["Astronaut", "Software Engineer"]), User(2, "John", "Doe", "jd@gmail.com", ["Astronaut"]), User(3, "Jane", "Doe", "jd1@gmail.com", ["Software Engineer"])]
		opportunities = [Opportunity(1, "Space X", ["Astronaut"], "elon@musk.com"), Opportunity(2, "Schmidt Futures", ["Software Engineer"], "sf@schmidtfutures.com")]
		
		matches = self.matcher.match(users, opportunities)

		assert len(matches) == 2
		assert len(self.matcher.get_unmatched_users()) == 1

if __name__ == '__main__':
	unittest.main()