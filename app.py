import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from bson import SON
from pprint import pprint
from pymongo import ASCENDING, TEXT, DESCENDING
from functions import get_pages, generate_pagination_links

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'cookbookdatabase'
app.config["MONGO_URI"] ="mongodb://admin:Komplete8@ds119150.mlab.com:19150/cookbookdatabase"
#os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def index():
    #Render Index Page
    return render_template("index.html")
    
@app.route('/recipes')
def recipes():
    
    # Get All Recipes
    recipes = mongo.db.recipes
    all_recipes = recipes.find()
    
    # Pagination Settings
    offset = 0 
    limit = int(request.args.get('limit'))
    
    #Get Count
    count_list = []
    for doc in all_recipes:
        count_list.append(doc)
        count = len(count_list)
    
    #Get Pages And Generate URL List
    pages = get_pages(count, limit)
    url_list = generate_pagination_links(offset, limit, pages, 'recipes', 'null')
    print(url_list)
    
    #Get _id of Last Item on a Page
    dynamic_position = request.args.get('offset')
    starting_id = recipes.find().sort('_id')
    last_id = starting_id[int(dynamic_position)]['_id']
    
    #Sort Tables
    sort_default = recipes.find({'_id' : {'$gte' : last_id}}).limit(limit)
    sort_country = recipes.find({'_id' : {'$gte' : last_id}}).sort([( "country", 1),
    ("name", 1 )]).limit(limit)
    sort_name = recipes.find({'_id' : {'$gte' : last_id}}).sort([("name",
    1 )]).limit(limit)
    sort_upvotes = recipes.find({'_id' : {'$gte' : last_id}}).sort([( "upvotes",
    pymongo.DESCENDING), ("name",1 )]).limit(limit)
    sort_downvotes = recipes.find({'_id' : {'$gte' : last_id}}).sort([( "downvotes",pymongo.DESCENDING), ("name", 1 )]).limit(limit)
    sort_author = recipes.find({'_id' : {'$gte' : last_id}}).sort([( "author",
    1), ("name", 1 )]).limit(limit)
   
    return render_template("recipes.html", author=sort_author, 
    default=sort_default, name=sort_name, upvotes=sort_upvotes, 
    downvotes= sort_downvotes, country=sort_country, url_list=url_list, 
    pages=pages)

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    #Get Details of Recipe
    the_recipe = mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    return render_template('edit_recipe.html', recipe=the_recipe)
   
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    #Get Recipes
    recipes = mongo.db.recipes
    
    #Get Info For Instructions,Ingredients and Allerges
    instructions = request.form.getlist('instruction2')
    ingredients = request.form.getlist('ingredient2')
    allergens = request.form.getlist('allergen2')
    
    #Carry Over Values for Non-Editable Attributes
    found = []
    cursor = recipes.find({ "_id": ObjectId(recipe_id)}, {"upvotes": 1, "downvotes": 1, "recipeID": 1 , '_id':0 })
    for document in cursor:
        found.append(document)
    
    #Update Existing Recipe
    recipes.update({'_id': ObjectId(recipe_id)},{
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': instructions,
            'upvotes': found[0]["upvotes"],
            'downvotes': found[0]["downvotes"],
            'ingredients': ingredients,
            'allergens': allergens,
            'country': request.form['country'],
            'author': request.form['author'],
            'recipeID': found[0]["recipeID"]
            })
            
    return redirect('/recipes?limit=10&offset=0')
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)