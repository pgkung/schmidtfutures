import json
import requests
from user import User
from opportunity import Opportunity

class DataLoader(object):

	def load_json_response_to_object(self, url, object):
		resp = requests.get(url=url)
		return json.loads(resp.text, object_hook=lambda data: object(**data))
	

	def get_users(self):
		return self.load_json_response_to_object('https://raw.githubusercontent.com/schmidtfutures/sf-eng-challenge/main/users.json', User)


	def get_opportunities(self):
		return self.load_json_response_to_object('https://raw.githubusercontent.com/schmidtfutures/sf-eng-challenge/main/opportunities.json', Opportunity)
