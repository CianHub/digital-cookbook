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

@app.route('/add_recipe')
def add_recipe():
    #Render Add Recipe Page
    return render_template("add_recipe.html")
 
@app.route('/insert_recipe', methods=['POST']) 
def insert_recipe():
    #Get Recipes
    recipes = mongo.db.recipes
    
    #Merge Additional Instruction Fields
    instructions = request.form.getlist('instruction2')
    instructions.insert(0, request.form['instruction1'])
    
    #Merge Additional Ingredients Fields
    ingredients = request.form.getlist('ingredient2')
    ingredients.insert(0, request.form['ingredient1'])
    
    #Merge Additional Allergens Fields
    allergens = request.form.getlist('allergen2')
    if request.form['allergen1'] != '':
        allergens.insert(0, request.form['allergen1'])
    
    #Insert New Recipe to Database
    recipes.insert(
        {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': instructions,
        'upvotes': 0,
        'downvotes': 0,
        'ingredients': ingredients,
        'allergens': allergens,
        'country': request.form['country'],
        'author': request.form['author'],
        'recipeID': (recipes.count() + 1)
        })
    return redirect('/recipes?limit=10&offset=0')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)