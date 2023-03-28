from flask import Flask
app =Flask(__name__)

@app.route("/")
def welcome():
    return "Hello World"

@app.route("/home")
def home():
    return "this is our home page"

# import controller.user_controller as user_controller,product_controller

from controller import *



