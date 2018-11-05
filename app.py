from flask import Flask, render_template, request, url_for, redirect, flash, session
import os,itertools
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from operator import itemgetter
import sys



"""
Mongodb connection and secert key
"""
app = Flask(__name__)
app.config['MONGO_DBNAME']='get-recipes'                                                     #mongo database name
app.config['MONGO_URI']='mongodb://admin:Kavitha2$@ds163730.mlab.com:63730/get-recipes'
app.secret_key = 'some_secret'

mongo = PyMongo(app)

"""
Home page with login form
"""
@app.route('/')
def index():
    return render_template('login.html', register=mongo.db.register.find_one())

"""
Register form action firsly, method must be post and we going to insert in database by given details from input in register.html 
and then It will redirect to get recipes
"""
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        register = mongo.db.register
        reg_id = register.insert_one(request.form.to_dict())
        # print(register)
        object_id = reg_id.inserted_id
        return redirect(url_for('get_recipe',register_id=object_id))
    return render_template('register.html')

"""
Login page action. Firstly, method must be post and we will find the given password and username if it match we will
redirect to get recipes if not redirect to register and if password only incorrect we will show password is incorrect
"""
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        login_user = mongo.db.register.find_one({'username': request.form['username']})
        form = request.form
        if login_user:
            if(form["password"] == login_user["password"]): # if password correct
                session['username'] = login_user["username"]
                return redirect(url_for('get_recipe',register_id = login_user["_id"]))
            else: # and if password is not correct
               flash("Incorrect password") 
        else:# if not exist
            flash("User does not exist")
            return redirect(url_for('register'))
    return render_template('login.html')
            
"""
Delete page action If user want to delete their account the information will remove from database
"""
@app.route('/delete_register/<register_id>',methods=["GET","POST"] )
def delete_register(register_id):
    mongo.db.register.remove({'_id':ObjectId(register_id)})
    return redirect(url_for('login'))

@app.route('/edit_recipes/<recipes_id>/<register_id>',methods=['POST','GET'])           # edit the recipe
def edit_recipes(recipes_id,register_id):
    recipes=mongo.db.recipes.find_one({'_id':ObjectId(recipes_id)})
    print(request.form.get('recipe_name'))
    return render_template('edit_recipes.html',recipes=recipes,register = mongo.db.register.find_one({'_id':ObjectId(register_id)}))
    
@app.route('/update_recipes/<recipes_id>/<register_id>',methods=['GET','POST'])
def update_recipes(recipes_id,register_id):
    # if request.method == "POST":
    recipes=mongo.db.recipes
    update = recipes.update({'_id':ObjectId(recipes_id)},  
    {          "name":request.form.get("name"),
               "ingredients":request.form.get("ingredients"),
                "steps":request.form.get("steps"),
                "imageURL":request.form.get("imageURL"),
                "creditTo":request.form.get("credit"),
                "preparation":request.form.get("preparation"),
                "cooking":request.form.get("cooking")})
    print(recipes)
    print(request.form.get('recipe_name'))
    print(update)
    return redirect(url_for('show_recipes', recipes_id=recipes_id,register_id=register_id))
    
@app.route('/edit_register/<register_id>', methods=['POST','GET'])
def edit_register(register_id):
    register=mongo.db.register.find_one({'_id':ObjectId(register_id)})
    print(register)
    return render_template('edit_register.html',register=register)

@app.route('/update_register/<register_id>', methods=['GET','POST'])
def update_register(register_id):
    register = mongo.db.register
    register.update({'_id':ObjectId(register_id)},{"username":request.form.get('username'),
               "email":request.form.get('email'),
               "password":request.form.get('password')})
    print(request.form.get('email'))
    return redirect('login')


@app.route('/get_recipe/<register_id>',methods=['POST','GET'])
def get_recipe(register_id):
    register = mongo.db.register.find_one({'_id':ObjectId(register_id)})
    
    return render_template('get_recipe.html',recipes=mongo.db.recipes.find(), register=register)

@app.route('/add_recipes/<register_id>',methods=['POST','GET'])
def add_recipes(register_id):
    print(register)
    print(request.form.get('recipe_name'))
    return render_template('add_recipes.html',recipes=mongo.db.recipes.find(), register = mongo.db.register.find_one({'_id':ObjectId(register_id)}))
    
@app.route('/insert_recipes/<register_id>', methods=["POST"])
def insert_recipes(register_id):
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
    register = mongo.db.register.find_one({'_id':ObjectId(register_id)})
    return redirect(url_for('get_recipe',register_id=register['_id']))

@app.route('/show_recipes/<recipes_id>/<register_id>',methods=['POST','GET'])
def show_recipes(recipes_id,register_id):
    recipes=mongo.db.recipes.find_one({'_id':ObjectId(recipes_id)})
    register = mongo.db.register.find_one({'_id':ObjectId(register_id)})
    return render_template('show_recipes.html',recipes=recipes,register=register )
    
@app.route('/search_recipes/<register_id>', methods=['POST','GET'])
def search_recipes(register_id):
    if request.method == "POST":
        recipes=list(mongo.db.recipes.find({"name": {"$regex":request.form['search']}}))
        print(recipes,request.form.get('search'))
        if recipes:
            return render_template('search_recipes.html', register=mongo.db.register.find_one({'_id':ObjectId(register_id)}), recipes=recipes)
        else:
            return render_template('404.html', register=mongo.db.register.find_one({'_id':ObjectId(register_id)}), recipes=recipes,message='No recipes found')
    return render_template('search_recipes.html', register=mongo.db.register.find_one({'_id':ObjectId(register_id)}), recipes=recipes)        
    
"""
Below code is for vote/like 
"""
@app.route('/vote/<recipes_id>', methods=["POST"])
def upvote(recipes_id): 
    mongo.db.recipes.update_one({"_id": ObjectId(recipes_id)}, {"$inc":
                                                               {'votes': 1}})
    return redirect(url_for('show_recipes', recipes_id=recipes_id,register_id=register['_id']))
    
    """
    Below code is for testing 
    """
recipes=mongo.db.recipes.find_one({'name':'Grilled chicken burgers'})
register=mongo.db.register.find_one({'username':'Ram'})
"""
host script
"""
if __name__ == "__main__":
    app.run(host=os.getenv('IP'),
        port= int(  os.getenv('PORT')),
        debug=True)