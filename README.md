# DIGITAL COOKBOOK 

Digital Cookbook is a responsive web application that allows users to create, give feedback on, update, delete and read cooking recipes.
 
## UX

### User Stories

Before beginning development on the site, several user stories were created to determine who a visitor to the site could be and what they might want from the site:

- "As a user I want to be able to search for recipes and add my own recipes for others to try under my own name."

- "As a user to the website, I want to be able to quickly browse a selection of recipes and let the author know what I thought."

### Design

The application utilises a minimal responsive design based upon a heavily modified version of the [creative bootstrap theme](https://startbootstrap.com/template-overviews/creative/), built around centered content on a background image. 

The key focus of the apps design was readability and simplicity. The text was designed to stand out, through the choice of colors in the content and the background image.

## Features

The application has several features:

1. Users can browse the recipes in the database manually, through search or by attribute.
2. Users can add their own recipes to the database.
3. Users can edit or delete existing recipes.
4. Users can upvote or downvote recipes.
5. Users can enter their username and view the recipes they have added.

## Technologies Used

- [HTML](https://www.w3.org/)
    - The project uses **HTML** to create the website.

- [CSS](https://www.w3.org/)
    - The project uses **CSS** to style the website.

- [Bootstrap](https://getbootstrap.com/docs/3.3/)
    - The project uses **Bootstrap** to style the site and user experience.

- [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript)
    - The project uses **JavaScript** to use Bootstrap functions.

- [JQuery](https://jquery.com/)
    - The project uses **JQuery** to manipulate the DOM with Bootstrap functionality.

- [Python](https://www.python.org/)
    - The project uses **Python** to write the sites logic.

- [Flask](http://flask.pocoo.org/)
    - The project uses **Flask** for the apps backend (server, load jinja2 templates etc.). 

- [MongoDB](https://www.mongodb.com/)
    - The project uses **MongoDB** as the apps database. 

## Testing

In the development of this application testing consisted of both automated tests using the python unittest package and manual testing of views.

### Automated Testing

 To run tests, in the CLI enter:
```
$ python -m unittest discover
``` 

### Manual Testing

Due to using flask_pymongo, I ran into some issues when trying to write automated tests for the projects views. As a result, testing on the views was conducted manually instead.

1. Home Page
    1. Go to the home page of the project.
    2. Verify the page loads with the index.html template.

2. Recipes Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Verify the view recipes page loads with the recipes.html template.

3. My Recipes Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'My Recipes' in the navbar
    4. Verify the My Recipes page loads with the results.html template or the noresults.html if there are no recipes associated with the username.

4. View Recipe Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'View Recipe' button from a recipe in the table of recipes.
    4. Verify the View Recipe page loads with the view_recipe.html template.

5. Edit Recipe Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'Edit Recipe' button from a recipe in the table of recipes.
    4. Verify the Edit Recipe page loads with the edit_recipe.html template.

6. Delete Recipe Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'Delete Recipe' button from a recipe in the table of recipes.
    4. Verify the Delete Recipe page loads with the delete_recipe.html template.

7. Add Recipe Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'Add Recipes' in the navbar
    4. Verify the Add Recipe page loads with the add_recipe.html template.

8. Search Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'Search' in the navbar
    4. Verify the Search page loads with the search.html template.

9. Results Page
    1. Go to the home page of the project.
    2. Enter a username and click enter.
    3. Click 'Search' in the navbar
    4. In the search page, search a term.
    5. Verify the results page loads with the results.html template or the noresults.html if there are no recipes associated with the search term.

## Planning

### Database Schema

The database schema for the app can be found in the file Digital Cookbook_ Database Schema included in this repository.

A MongoDB based NoSQL database was chosen to keep the database schema as simple possible. When drawing up the schema, the aim was to keep the most relevent fields while ensuring the user didn't feel restricted. The other major consideration was the data types, these were carefully selected in order to make accessing the values as easy as possible for CRUD functions while still being dynamic. 

For example, as it is impossible to predict how many ingredients, instructions or allergens a recipe could have, a list format made the most sense from a 'create' perspective, this too made sense for 'update' operations as a list can be lengthened or shortened easily. Lastly a list also works well with 'read' operations as the individual indices of a list can be searched by the user.

Finally there were smaller considerations such as readability taken into account. For example, a recipeID of '2' is a lot easier to read/remember than an _id of '5af74281f36d280cecd216c3' in a URL bar!

### Preliminary Planning Document

The preliminary planning conducted before development began (including user stories, outline of functionality, site map etc.) can be found in the repository under the name Digital Cookbook_Preliminary Planning.pdf.

## Deployment

This project was deployed to Heroku. Inside Heroku's config vars the DBNAME, IP, PORT, SECRET (secret key) and URI (MongoDB uri) were set. 

The Project can be viewed at: <https://riddle-me-this-game.herokuapp.com/>

## Installation

1. Ensure Python3, pip and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder.
5. Setup the virtualenv instance for the project and activate the virtualenv instance. 
7. Install required packages from requirements.txt. 
8. Set DBNAME (name of MongoDB database), SECRET (secret key) and URI (MongoDB URI) environmental variables.
8. Run run.py .

## Credits

### Acknowledgements

- The projects design is based on a heavily modified version of the [creative bootstrap theme](https://startbootstrap.com/template-overviews/creative/)
