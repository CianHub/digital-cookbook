import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from bson import SON
from pprint import pprint
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
from functions import get_pages, generatePaginationLinks

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
    url_list = generatePaginationLinks(offset, limit, pages, 'recipes', 'null')
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

@app.route('/search', methods=['GET','POST'])
def search():
    #Search User Input
        if request.method == "POST":
            return redirect('/' + 'search' + '/' + request.form["search"] + '?limit=10&offset=0')
        return render_template("search.html")
    
@app.route('/search/<search>', methods=['GET','POST'] )
def results(search):
    
    # Get All Recipes
    recipes = mongo.db.recipes
    found_recipes = recipes.find({"$text": {"$search": str(search)}})
    
    # Pagination Settings
    limit = int(request.args.get('limit'))
    offset = 0 
    
    #Get Count
    count_list = []
    for doc in found_recipes:
        count_list.append(doc)
        count = len(count_list)
    
    #If No Results Found
    if len(count_list) < 1:
        return render_template('noresults.html')
    
    #Get Pages And Generate URL List
    pages = get_pages(count, limit)
    url_list = generatePaginationLinks(offset, limit, pages, 'search', search)

    #Get _id of Last Item on a Page
    dynamic_position = request.args.get('offset')
    starting_id = recipes.find({"$text": {"$search": str(search)}}).sort('_id')
    last_id = starting_id[int(dynamic_position)]['_id']
    
    #Sort Tables
    sort_default = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).limit(limit)
    sort_country = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("country",1),("name",1 )]).limit(limit)
    sort_name = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("name", 1)]).limit(limit)
    sort_upvotes = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("upvotes",
    pymongo.DESCENDING),("name",1 )]).limit(limit)
    sort_downvotes = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("downvotes",pymongo.DESCENDING),("name",1 )]).limit(limit)
    sort_author = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("author",1),("name",1 )]).limit(limit)

    return render_template("results.html", default=sort_default, count=count, 
    url_list=url_list, pages=pages, search=search, country=sort_country, name=sort_name, 
    upvotes=sort_upvotes, downvotes=sort_downvotes, author=sort_author)

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

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    #Get Details of Recipe
    the_recipe = mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    return render_template('edit_recipe.html', recipe=the_recipe)

@app.route('/view_recipe/<recipe_id>', methods=['GET','POST'])
def view_recipe(recipe_id):
    #Get Recipes
    recipes = mongo.db.recipes
    
    #Get Details of Selected Recipe
    the_recipe = mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    #Store Details of Selected Recipe
    current_recipe = []
    for i in the_recipe:
        current_recipe.append({i : the_recipe[i]})
    current = sorted(current_recipe)
    
    #If a Button is Pressed
    if request.method == "POST":
        
        #If Upvote
        if request.form['vote'] == "upvote":
            
            #Increment Upvote
            current[10]['upvotes'] += 1
            
            #Update Existing Attributes
            recipes.update({'_id': ObjectId(recipe_id)},
            {
                'name': current[8]['name'],
                'description': current[4]['description'],
                'instructions': current[7]['instructions'],
                'upvotes': current[10]['upvotes'],
                'downvotes': current[5]["downvotes"],
                'ingredients': current[6]['ingredients'],
                'allergens': current[1]['allergens'],
                'country': current[3]['country'],
                'author': current[2]['author'],
                'recipeID': current[9]["recipeID"]
            })
         
        #If Downvote 
        elif request.form['vote'] == "downvote":
            
            #Increment Downvote
            current[5]['downvotes'] += 1
            
            #Update Existing Attributes
            recipes.update({'_id': ObjectId(recipe_id)},
            {
                'name': current[8]['name'],
                'description': current[4]['description'],
                'instructions': current[7]['instructions'],
                'upvotes': current[10]['upvotes'],
                'downvotes': current[5]["downvotes"],
                'ingredients': current[6]['ingredients'],
                'allergens': current[1]['allergens'],
                'country': current[3]['country'],
                'author': current[2]['author'],
                'recipeID': current[9]["recipeID"]
            })
         
            
    return render_template('view_recipe.html', recipe=the_recipe)
    
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