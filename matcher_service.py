from flask import Flask
from matcher import Matcher
from data_loader import DataLoader
import json

app = Flask(__name__)
matcher = Matcher()

@app.before_first_request
def calculate_matches():
	data_loader = DataLoader()
	users = data_loader.get_users()
	opportunities = data_loader.get_opportunities()
	matcher.match(users, opportunities)

@app.route("/matches")
def matches():
	all_matches = matcher.get_matches()
	return json.dumps(all_matches, default=lambda o: o.__dict__)

@app.route("/matches/users/")
def match_by_user():
	match_by_user = matcher.get_matches_by_user()
	return json.dumps(match_by_user, default=lambda o: o.__dict__)

@app.route("/matches/users/<user_id>")
def match_by_user_id(user_id):
	try:
		match_for_user = matcher.get_match_for_user(int(user_id))
	except:
		return "User ID must be an integer", 400
	return json.dumps(match_for_user, default=lambda o: o.__dict__)

@app.route("/matches/opportunities/")
def matches_by_opportunity():
	matches_by_opportunity = matcher.get_matches_by_opportunities()
	return json.dumps(matches_by_opportunity, default=lambda o: o.__dict__)

@app.route("/matches/opportunities/<opportunity_id>")
def match_by_opportunity_id(opportunity_id):
	try: 
		matches_for_opportuity = matcher.get_matches_for_opportunity(int(opportunity_id))
	except:
		return "Opportunity ID must be an integer", 400
	return json.dumps(matches_for_opportuity, default=lambda o: o.__dict__)

@app.route("/matches/unmatched/users")
def unmatched_users():
	unmatched_users = matcher.get_unmatched_users()
	return json.dumps(unmatched_users, default=lambda o: o.__dict__)

@app.route("/matches/unmatched/opportunities")
def unmatched_opportunities():
	unmatched_opportunities = matcher.get_unmatched_opportunities()
	return json.dumps(unmatched_opportunities, default=lambda o: o.__dict__)
