from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'This will be a volleyboard dashball. Or something like that'
