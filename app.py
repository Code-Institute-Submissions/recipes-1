from flask import Flask, render_template, request, url_for, redirect
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config['MONGO_DBNAME']='get-recipes'
app.config['MONGO_URI']='mongodb://admin:Kavitha2$@ds163730.mlab.com:63730/get-recipes'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('register.html', register=mongo.db.register.find_one())
    
@app.route('/register',methods=["POST"])
def register():
    register = mongo.db.register
    register.insert_one(request.form.to_dict())
    print(register)
    return redirect('/get_recipe')


@app.route('/login', methods=["POST","GET"])
def login():
    register = mongo.db.register.find({''})
    log_doc = {'username':request.form.get('username'),
                'password':request.form.get('password')
    }
    if register == log_doc:
        print('welcome',register,log_doc)
    else:
        print('Error',register,log_doc)
        return redirect('/')
    return render_template('login.html', register = mongo.db.register.find())   

 
@app.route('/get_recipe')
def get_recipe():
    return render_template('get_recipe.html',recipes=mongo.db.recipes.find())
@app.route('/add_recipes')
def add_recipes():
    return render_template('add_recipes.html',recipes=mongo.db.recipes.find() )
    
@app.route('/insert_recipes', methods=["POST"])
def insert_recipes():
    recipes = mongo.db.recipes
    recipes_doc = {"name":request.form.get('name'),
                    "ingredients":request.form.get('ingredients'),
                    "steps":request.form.get('steps'),
                    "imageURL":request.form.get('imageURL'),
                    "creditTo":request.form.get('credit'),
                    "preparation":request.form.get('preparation'),
                    "cooking":request.form.get('cooking')
    }  
    recipes.insert_one(recipes_doc)
    print(recipes)
    return redirect('/get_recipe')

@app.route('/show_recipes/<recipes_id>')
def show_recipes(recipes_id):
    recipes=mongo.db.recipes.find({'_id':ObjectId(recipes_id)})
    return render_template('show_recipes.html',recipes=recipes)

if __name__ == "__main__":
    app.run(host=os.getenv('IP'),
        port= int(  os.getenv('PORT')),
        debug=True)