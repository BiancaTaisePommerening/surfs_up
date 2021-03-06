#  import the Flask dependency
from flask import Flask
# Create a New Flask App Instance
app = Flask(__name__)
# create Flask Routes
@app.route('/')
# create a function called hello_world()
def hello_world():
    return 'Hello world'
# create a new route and new function.
@app.route('/test')
def test():
    return 'Running test'
