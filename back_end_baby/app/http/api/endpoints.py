from flask import Flask, json, g, request
from app.event.service import Service
from app.event.schema import GithubRepoSchema
from flask_cors import CORS
import app.yelp.interface as yelp

app = Flask(__name__)
CORS(app)


@app.route("/search_restaurant", methods=["GET"])
def restaurant_search():
    search_string = request.args["search_string"]
    location_string = request.args["location_string"]
    num_responses=10
    yelp_responses =  yelp.search(search_string, location_string, num_responses, sort_by='rating')
    return json_response(yelp_responses)


@app.route("/login/<int: event_id>", methods=["POST"])
def login(event_id):
    payload = {}
    userID = Service.getUserID(event_id)
    payload["user_id"] = userID
    #expect dictionary as response from getRestaurantVotes
    user_votes = Service.getRestaurantVotes(event_id, userID)
    payload["restaurant_votes"] = user_votes
    return json_response(userID)


@app.route("/kudos", methods=["POST"])
@login_required
def create():
   github_repo = GithubRepoSchema().load(json.loads(request.data))

   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo = Kudo(g.user).create_kudo_for(github_repo)
   return json_response(kudo)


@app.route("/kudo/<int:repo_id>", methods=["GET"])
@login_required
def show(repo_id):
 kudo = Kudo(g.user).find_kudo(repo_id)

 if kudo:
   return json_response(kudo)
 else:
   return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["PUT"])
@login_required
def update(repo_id):
   github_repo = GithubRepoSchema().load(json.loads(request.data))

   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo_service = Kudo(g.user)
   if kudo_service.update_kudo_with(repo_id, github_repo):
     return json_response(github_repo.data)
   else:
     return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
@login_required
def delete(repo_id):
 kudo_service = Kudo(g.user)
 if kudo_service.delete_kudo_for(repo_id):
   return json_response({})
 else:
   return json_response({'error': 'kudo not found'}, 404)


def json_response(payload, status=200):
 return (json.dumps(payload), status, {'content-type': 'application/json'})
