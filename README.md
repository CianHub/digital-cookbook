# DIGITAL COOKBOOK 

Digital Cookbook is a responsive web application that allows users to create, give feedback on, update, delete and read cooking recipes.

## Features

The application has several features:

1. Users can browse the recipes in the database manually, through search or by attribute.
2. Users can add their own recipes to the database.
3. Users can edit or delete existing recipes.
4. Users can upvote or downvote recipes.
5. Users can enter their username and view the recipes they have added.

## Technologies

The application was developed with MongoDB, Flask, Python3, HTML5, CSS3, JavaScript, JQuery and Bootstrap.

## Installation

1. Ensure Python3, pip, MongoDB and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder
5. Setup the virtualenv instance for the project and activate the virtualenv instance 
7. Install required packages from requirements.txt 
8. Run app.py 

## Testing

To run tests, in the CLI enter:
```
$ python -m unittest discover
```

## Database Schema

The database schema for the app can be found in the file Digital Cookbook_ Database Schema included in this repository.

A MongoDB based NoSQL database was chosen to keep the database schema as simple possible. When drawing up the schema, the aim was to keep the most relevent fields while ensuring the user didn't feel restricted. The other major consideration was the data types, these were carefully selected in order to make accessing the values as easy as possible for CRUD functions while still being dynamic. 

For example, as it is impossible to predict how many ingredients, instructions or allergens a recipe could have, a list format made the most sense from a 'create' perspective, this too made sense for 'update' operations as a list can be lengthened or shortened easily. Lastly a list also works well with 'read' operations as the individual indices of a list can be searched by the user.

Finally there were smaller considerations such as readability taken into account. For example, a recipeID of '2' is a lot easier to read/remember than an _id of '5af74281f36d280cecd216c3' in a URL bar!

## Deployment

The application was deployed to Heroku and can be viewed at: <https://online-cookbook-project.herokuapp.com/>
