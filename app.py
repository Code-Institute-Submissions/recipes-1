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
    return render_template('register.html', reg=mongo.db.register.find_one())
    
@app.route('/register',methods=["POST"])
def register():
    register = mongo.db.register
    register.insert_one(request.form.to_dict())
    print(register)
    return redirect('/')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(host=os.getenv('IP'),
        port= int(  os.getenv('PORT')),
        debug=True)