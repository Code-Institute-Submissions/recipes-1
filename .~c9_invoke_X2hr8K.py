from flask import Flask, render_template, request, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
    render_template('')

if __name__ == "__main__":
    app.run(host=os.getenv('IP'),
        port= int(  os.getenv('PORT')),
        debug=True)