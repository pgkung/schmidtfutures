# User and Opportunity Matching
Attempts to calculate reasonable matches given users with interests and opportunities with open roles.

## Background and Motivations
The idea of this project is to get a baseline match down which should then be manually reviewed. This matching problem is similar to the stable marriage problem which is notably solvable with the Gale-Shapley algorithm. The slight differences here make it hard to apply the algorithm exactly, but we can still take inspiration from it. 

The notable differences are:
- Opportunities can have multiple matches
- There's no strict ranking that an opportunity would have for a given user/applicant

This project assumes the users list their interests in order from most interested to least. The two core ideas behind this project is to:
* Have the most matches possible
* Give the user their top preference when possible

The drawback of the current approach is that it starts with users and opportunites with least amount of interests and roles to ensure the most matches meaning it's biased towards those providing less info. If users and organizations knew about this they would be encouraged to include less interests and roles in order to get what they want.

## Running the app
This is a python 3 flask app which requires the Request and Flask module to start. I would recommend creating a virtual environment to do so which you can read more about [here](https://flask.palletsprojects.com/en/2.1.x/installation/#virtual-environments)

To install the modules run:
`pip install requests Flask`

To run the service we need to set the environment variable for Flask and then run the app
```
export FLASK_APP=matcher_service
flask run
```
The app should now be running on localhost:5000

## Functionality
`GET /matches` Returns a JSON list of all matches (a user object followed by an opportunity object)
`GET /matches/users` Returns a JSON list of all matches grouped by user (effectively the same as /matches currently)
`GET /matches/opportunites` Returns a JSON list of all matches grouped by opportunities
`GET /matches/users/<user_id>` Returns a JSON of all matches for the given user_id integer
`GET /matches/opportunities/<user_id>` Returns a JSON of all matches for the given opportunity_id integer
`GET /matches/unmatched/users` Returns a JSON list of all remaining umatched users
`GET /matches/unmatched/opportunities` Returns a JSON list of all remaining umatched opportunities

## Later revisions
Some ideas for improvements and nice to haves for future iterations would include:
 - Database support
 - Displaying a diff of what would change if the current matching is applied (roles left open, people left unmatched, etc)
 - Support paging through the matches
 - Allow for manual overrides i.e force certain matches and have the matcher recalculate around that
 - Handle concurrency i.e allow two users to update things simultaneously 
 - Handle more types of ranking and quotas i.e two spots may be open for one role, maybe the organizations could rank applicants in some way as well
