from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
from pymongo import MongoClient
import json

# Initialize the Flask application
app = Flask(__name__)

# define all of the endpoints
@app.route('/api/list_recipes', methods=['GET'])
def list_recipes():
    found = list(recipes.find({}))
    return Response(response=jsonpickle.encode(found), status=200, mimetype="application/json")

@app.route('/api/get_recipe/<name>', methods=['GET'])
def get_recipe(name):
    found = recipes.find_one({"name" : name})
    return Response(response=jsonpickle.encode(found), status=200, mimetype="application/json")

@app.route('/api/find_ingredients', methods=['POST'])
def find_ingredients():
    ingred = json.loads(request.data)
    found = list(recipes.find({"$and" : ingred}))   
    return Response(response=jsonpickle.encode(found), status=200, mimetype="application/json")

@app.route('/api/add_recipe', methods=['POST'])
def add_recipe():
    recipe = json.loads(request.data)
    recipes.insert_one(recipe)  
    return Response(response=jsonpickle.encode(1), status=200, mimetype="application/json")

@app.route('/api/add_review/<name>', methods=['POST'])
def add_review(name):
    review = json.loads(request.data)
    recipes.update_one({"name" : name}, {"$push" : {"ratings" : review['rating']}})
    recipes.update_one({"name" : name}, {"$push" : {"comments" : review['comment']}})
    return Response(response=jsonpickle.encode(1), status=200, mimetype="application/json")


# get username and password from user to authenticate
username = input("Username: ")
password = input("Password: ")

# authenticate user and run flask or throw error and exit
try:
    # connect to db and get recipes
    client = MongoClient("mongodb+srv://"+username+":"+password+"@cluster0.x57xj.mongodb.net/<dbname>?retryWrites=true&w=majority")
    client.server_info()
    db = client.get_database("recipe_book")
    recipes = db.recipes
    
    # start flask app
    app.run(host="0.0.0.0", port=5000)
except:
    print("Failed to connect to server.")
