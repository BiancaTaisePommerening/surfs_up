#  import the Flask dependency
from flask import Flask
# Create a New Flask App Instance
app = Flask(__name__)
# create Flask Routes
@app.route('/')
# create a function called hello_world()
@app.route('/')
def hello_world():
    return 'Hello world'