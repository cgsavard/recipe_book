from __future__ import print_function
import requests
import json
import sys
import jsonpickle

#-----------------------------
# HELPER FUNCTIONS
#-----------------------------

# list all service options the user can choose  
def list_options():
    print("Services include:")
    print("\tlist_recipes (get list of all recipes)")
    print("\tget_recipe (get a single recipe by name)")
    print("\tfind_ingredients (get recipes from certain ingredients)")
    print("\tadd_recipe (add a recipe to memory)")
    print("\tadd_review (add a review to a certain recipe)")

# print out the recipe for the user to use
def print_recipe(recipe):
    # recipe name
    print("\n",recipe['name'],"(",recipe['minutes'],"minutes )","\n")

    # ingredients
    print("Ingredients:")
    for i in recipe['ingredients']:
        print("\t",i)
    print("\n")

    # steps
    print("Steps:")
    count = 1
    for s in recipe['steps']:
        print("\t",count,")",s)
        count += 1
    print("\n")

    # reviews
    print("Reviews:")
    if recipe['ratings']==[]:
        print("\tNo reviews yet. Be the first to add one with the add_review service!")
    else:
        print("\tAverage rating =",sum(recipe['ratings'])/len(recipe['ratings']),"\n")
        print("\tRating\tComment")
        for (r,c) in zip(recipe['ratings'],recipe['comments']):
            print("\t",r,"\t",c)
    print("\n")


#-----------------------------
# FIND SERVICE
#-----------------------------

# read in the service the user wants to use
addr = "http://127.0.0.1:5000"    
try:
    service = sys.argv[1]
except:
    service = None    

#-----------------------------
# SERVICE: HELP
#-----------------------------
    
if service=='help':
    list_options()

#-----------------------------
# SERVICE: LIST_RECIPES
#-----------------------------

elif service=='list_recipes':
    url = addr+"/api/"+service
    response = requests.get(url)
    recipes = json.loads(response.text)

    letter = input("Enter a letter to look at the recipes alphabetically: ")

    print("Recipes available:")
    for r in recipes:
        try:
            if r["name"][0].lower() == letter.lower():
                print("\t",r["name"])
        except:
            continue
    print("Take a look at one of the above recipes by using the 'get_recipe' service.")

#-----------------------------
# SERVICE: GET_RECIPE
#-----------------------------

elif service=='get_recipe':
    name = input("Recipe name: ")
    url = addr+"/api/"+service+"/"+name
    response = requests.get(url)
    recipe = json.loads(response.text)

    if recipe==None:
        print("Recipe not found.")
        print("Please use the 'list_recipes' service to get a list of all recipes available.")
    else:
        print_recipe(recipe)

#-----------------------------
# SERVICE: FIND_INGREDIENTS
#-----------------------------

elif service=='find_ingredients':
    ingred = [{ "ingredients" : item.strip(' ') } for item in input("Enter the ingredients with a comma space between each, then press 'enter': ").split(',') ]
        
    url = addr+"/api/"+service

    headers = {'content-type': 'application/json'}
    data = json.dumps(ingred)
    response = requests.post(url, data=data, headers=headers)
    recipes = json.loads(response.text)

    if recipes==[]:
        print("Recipes not found, try a subset of those ingredients")
    else:
        print("Recipes found which match your required ingredients:")
        for r in recipes:
            print("\t",r['name'])
        print("Take a look at one of the above recipes by using the 'get_recipe' service.")

#-----------------------------
# SERVICE: ADD_RECIPE
#-----------------------------

elif service=='add_recipe':
    name = input("Recipe name: ")
    minutes = int(input("Cook time (minutes): "))
    ingredients = [ingred.strip(' ') for ingred in input("Ingredients (include a comma between each ingredient): ").split(',')]
    n_ingredients = len(ingredients)
    steps = [step.strip(' ') for step in input("Steps (include a comma between each step): ").split(',')]
    n_steps = len(steps)

    recipe = {"name" : name, "minutes" : minutes, "n_steps" : n_steps, "steps" : steps, "n_ingredients" : n_ingredients, "ingredients" : ingredients, "ratings" : [], "comments" : []}
    
    data = json.dumps(recipe)
    headers = {'content-type': 'application/json'}
    url = addr+"/api/"+service
    response = requests.post(url, data=data, headers=headers)

#-----------------------------
# SERVICE: ADD_REVIEW
#-----------------------------

elif service=='add_review':
    name = input("Recipe name: ")
    rating = float(input("Rating (out of 5): "))
    comment = input("Type out a review, then press enter: ")
    review = {"rating" : rating, "comment" : comment}
    
    data = json.dumps(review)
    headers = {'content-type': 'application/json'}
    url = addr+"/api/"+service+"/"+name
    response = requests.post(url, data=data, headers=headers)

#-----------------------------
# SERVICE: INVALID RESPONSE
#-----------------------------
        
else:
    print("Invalid service, please try again.")
    list_options()
