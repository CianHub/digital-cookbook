import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from bson import SON
from pprint import pprint
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
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
    url_list = generate_pagination_links(offset, limit, pages, 'search', search)

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
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)