from flask import Flask

import requests

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    # response = requests.get("http://name-generator-app-service/")
    # name = response.text
    
    # return 'Hello, World!' + name
    return 'Hello, World!'

# Run the app if this script is executed
if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True, port=8080)