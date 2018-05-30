from flask_wtf import FlaskForm, Form
from wtforms import  TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from utils import get_countries

country_list = get_countries()

class ReusableForm(Form):
    
    #Set up form
    name = TextField('Recipe Name:', validators=[validators.DataRequired("*Required")])
    description = TextField('Description:', validators=[validators.DataRequired("*Required")])
    author = TextField('Author:', validators=[validators.DataRequired("*Required")])
    instruction1 = TextField('Step 1:', validators=[validators.DataRequired("*Required")])
    ingredient1 = TextField( validators=[validators.DataRequired("*Required")])
    country = SelectField('Country of Origin', choices=country_list, validators=[validators.InputRequired(message=('*Required'))]) 

class Username(Form):
    #Set up form
    username = TextField('Username:', validators=[validators.DataRequired("*Required")])

class Search(Form):
    #Set up form
    search = TextField('Search:', validators=[validators.DataRequired("*Required")])