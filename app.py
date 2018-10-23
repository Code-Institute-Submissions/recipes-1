from flask import Flask, render_template, request, url_for, redirect, flash, session
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config['MONGO_DBNAME']='get-recipes'
app.config['MONGO_URI']='mongodb://admin:Kavitha2$@ds163730.mlab.com:63730/get-recipes'
app.secret_key = 'some_secret'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('login.html', register=mongo.db.register.find_one())

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        register = mongo.db.register
        register.insert_one(request.form.to_dict())
        print(register)
        return redirect('/get_recipe','register_id=register._id')
    return render_template('register.html')

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
            
            
@app.route('/delete_register/<register_id>',methods=["GET","POST"] )
def delete_register(register_id):
    mongo.db.register.remove({'_id':ObjectId(register_id)})
    return redirect(url_for('login'))

@app.route('/edit_recipes/<recipes_id>/<register_id>',methods=['POST','GET'])
def edit_recipes(recipes_id,register_id):
    recipes=mongo.db.recipes.find_one({'_id':ObjectId(recipes_id)})
    return render_template('edit_recipes.html',recipes=recipes,register = mongo.db.register.find_one({'_id':ObjectId(register_id)}))
    
@app.route('/update_recipes/<recipes_id>',methods=['POST'])
def update_recipes(recipes_id):
    recipes=mongo.db.recipes
    recipes.update({'_id':ObjectId(recipes_id)},{"name":request.form.get('name'),
                    "ingredients":request.form.get('ingredients'),
                    "steps":request.form.get('steps'),
                    "imageURL":request.form.get('imageURL'),
                    "creditTo":request.form.get('credit'),
                    "preparation":request.form.get('preparation'),
                    "cooking":request.form.get('cooking')
    } )
    return redirect(url_for('get_recipe'))
    
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
    return redirect('login',)
    
@app.route('/get_recipe/<register_id>',methods=['POST','GET'])
def get_recipe(register_id):
    register = mongo.db.register.find_one({'_id':ObjectId(register_id)})
    return render_template('get_recipe.html',recipes=mongo.db.recipes.find(), register=register)
@app.route('/add_recipes/<register_id>',methods=['POST','GET'])
def add_recipes(register_id):
    print(register)
    return render_template('add_recipes.html',recipes=mongo.db.recipes.find(), register = mongo.db.register.find_one({'_id':ObjectId(register_id)}))
    
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

@app.route('/show_recipes/<recipes_id>',methods=['POST','GET'])
def show_recipes(recipes_id):
    recipes=mongo.db.recipes.find({'_id':ObjectId(recipes_id)})
    return render_template('show_recipes.html',recipes=recipes, register = mongo.db.register.find_one())
    
@app.route('/search_recipes/<register_id>', methods=['POST','GET'])
def search_recipes(register_id):
    query = { "name": { "$regex": request.form.get('search') } }
    recipes = mongo.db.recipes.find_one(query)
    return render_template('search_recipes.html',register = mongo.db.register.find_one({'_id':ObjectId(register_id)}), recipes= recipes )

@app.route('/vote/<recipes_id>', methods=["POST"])
def upvote(recipes_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipes_id)}, {"$inc":
                                                               {'votes': 1}})
        
    return redirect(url_for('show_recipes', recipes_id=recipes_id))
if __name__ == "__main__":
    app.run(host=os.getenv('IP'),
        port= int(  os.getenv('PORT')),
        debug=True)