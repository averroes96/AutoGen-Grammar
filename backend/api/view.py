from flask import Blueprint

main = Blueprint(__name__)

@main.route("/home")
def home():

    return "Done", 201