import os
from os import environ
from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from flask_pymongo import PyMongo, pymongo
from dotenv import load_dotenv, find_dotenv
from bson.objectid import ObjectId
from bson import SON
from pprint import pprint
from pymongo import ASCENDING, DESCENDING, TEXT
from utils import get_pages, generate_pagination_links, get_countries
from flask_wtf import FlaskForm, Form
from wtforms import  TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from forms import Username, ReusableForm, Search

load_dotenv(find_dotenv())

app = Flask(__name__)

#For Local .env file
app.secret_key = os.getenv('SECRET')

app.config["MONGO_DBNAME"] = os.getenv('DBNAME')
app.config["MONGO_URI"] = os.getenv('URI')

#For Heroku 
app.secret_key = os.environ['SECRET']

app.config["MONGO_DBNAME"] = os.environ['DBNAME']
app.config["MONGO_URI"] = os.environ['URI']

mongo = PyMongo(app)

@app.route('/', methods=['GET','POST'])
def index():
    #Username form
    wtform = Username(request.form)
    if wtform.validate():
        return redirect('/' + request.form['username'] + '/recipes?limit=10&offset=0')
    
    return render_template("index.html", form=wtform, errors=wtform.errors)
    
@app.route('/<username>/recipes')
def recipes(username):
    
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
    url_list = generate_pagination_links(offset, limit, pages, 'recipes', 'null', username)

    #Get _id of Last Item on a Page
    dynamic_position = request.args.get('offset')
    starting_id = recipes.find().sort('_id')
    last_id = starting_id[int(dynamic_position)]['_id']
    
    #Sort Tables
    sort_default = recipes.find({'_id' : {'$gte' : last_id}}).sort([( "upvotes",
    pymongo.DESCENDING), ("downvotes",1 ), ('name', 1)]).limit(limit).limit(limit)
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
    pages=pages, username=username)

@app.route('/<username>/search', methods=['GET','POST'])
def search(username):
    #Search User Input
        wtform = Search(request.form)
        if wtform.validate():
            return redirect('/' + username + '/' + 'search' + '/' + request.form["search"] + '?limit=10&offset=0')
        return render_template("search.html", username=username, form=wtform, errors=wtform.errors )
    
@app.route('/<username>/search/<search>', methods=['GET','POST'] )
def results(username, search):
    
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
    if len(count_list) < 1 or not search:
        return render_template('noresults.html', username=username)
    
    #Get Pages And Generate URL List
    pages = get_pages(count, limit)
    url_list = generate_pagination_links(offset, limit, pages, 'search', search, username)

    #Get _id of Last Item on a Page
    dynamic_position = request.args.get('offset')
    starting_id = recipes.find({"$text": {"$search": str(search)}}).sort('_id')
    last_id = starting_id[int(dynamic_position)]['_id']
    
    #Sort Tables
    sort_default = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([('_id',pymongo.DESCENDING)]).limit(limit)
    sort_country = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("country",1),("name",1 )]).limit(limit)
    sort_name = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("name", 1)]).limit(limit)
    sort_upvotes = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("upvotes",
    pymongo.DESCENDING),("name",1 )]).limit(limit)
    sort_downvotes = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("downvotes",pymongo.DESCENDING),("name",1 )]).limit(limit)
    sort_author = recipes.find({"$and":[{'_id':{'$gte' : last_id}},{"$text":{"$search": str(search)}}]}).sort([("author",1),("name",1 )]).limit(limit)

    return render_template("results.html", default=sort_default, count=count, 
    url_list=url_list, pages=pages, search=search, country=sort_country, name=sort_name, 
    upvotes=sort_upvotes, downvotes=sort_downvotes, author=sort_author, username=username)

@app.route('/<username>/add_recipe',methods=['GET','POST']  )
def add_recipe(username):
   #Load form
    wtform = ReusableForm(request.form)
    
    if wtform.validate():
        
        # Get All Recipes
        recipes = mongo.db.recipes
        all_recipes = recipes.find()
        
        #Get The Highest recipeID
        count_list = []
        for doc in all_recipes:
            count_list.append(doc['recipeID'])
            sort_count_list = sorted(count_list)

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
        'recipeID': ((sort_count_list[-1] + 1))
        })
        
        return redirect('/' + username + '/' + 'search' + '/' + username + '?limit=10&offset=0')

    #Render Add Recipe Page
    return render_template("add_recipe.html", form=wtform, errors=wtform.errors, username=username)
 
@app.route('/<username>/edit_recipe/<recipe_id>', methods=["GET",'POST'])
def edit_recipe(username, recipe_id):
    #Load form
    wtform = ReusableForm(request.form)
    
    #Get Details of Recipe
    the_recipe = mongo.db.recipes.find_one({"recipeID":int(recipe_id)})
    
    if wtform.validate():
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
    
        #Carry Over Values for Non-Editable Attributes
        found = []
        cursor = recipes.find({ "recipeID": int(recipe_id)}, {"upvotes": 1, "downvotes": 1, '_id':1 })
        for document in cursor:
            found.append(document)
    
        #Update Existing Recipe
        recipes.update({'_id': found[0]["_id"]},{
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': instructions,
            'upvotes': found[0]["upvotes"],
            'downvotes': found[0]["downvotes"],
            'ingredients': ingredients,
            'allergens': allergens,
            'country': request.form['country'],
            'author': request.form['author'],
            'recipeID': int(recipe_id)
            })
            
        return redirect('/' + username + '/recipes?limit=10&offset=0')
    
    return render_template('edit_recipe.html', recipe=the_recipe,   form=wtform, username=username)

@app.route('/<username>/delete_recipe/<recipe_id>')
def delete_recipe(username, recipe_id):
    #Remove Recipe
    mongo.db.recipes.remove({"recipeID":int(recipe_id)})
    return redirect(request.referrer)
 
@app.route('/<username>/view_recipe/<recipe_id>', methods=['GET','POST'])
def view_recipe(username, recipe_id):
    
    #Get Recipes
    recipes = mongo.db.recipes
    
    #Get Details of Selected Recipe
    the_recipe = mongo.db.recipes.find_one({"recipeID":int(recipe_id)})
    
    #Get Voting Details of Selected Recipe
    the_recipe_vote = mongo.db.recipes.find_one({"recipeID":int(recipe_id)}, { 'upvotes': 1, 'downvotes': 1 })
 
    #If a Button is Pressed
    if request.method == "POST":
        
        #Store Voting Details of Selected Recipe
        current = []
        for i in the_recipe_vote:
            current.append({i :the_recipe_vote[i]})
        
        #If Upvote
        if request.form['vote'] == "upvote":
            
            #Increment Field
            for x in current:
                if x.keys() == ['upvotes']:
                    new_vote = x['upvotes'] + 1
                    
            #Update Field
            recipes.update({'recipeID': int(recipe_id) },{ '$set':{ 'upvotes' : new_vote}})
    
            return redirect('/' + username + '/recipes?limit=10&offset=0')
         
        #If Downvote 
        elif request.form['vote'] == "downvote":
            
            #Increment Field
            for x in current:
                if x.keys() == ['downvotes']:
                    new_vote = x['downvotes'] + 1
            
            #Update Field
            recipes.update( {'recipeID': int(recipe_id) }, { '$set': { 'downvotes' : new_vote } } )
            
            return redirect('/' + username + '/recipes?limit=10&offset=0')
         
    return render_template('view_recipe.html', recipe=the_recipe, username=username) 
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)