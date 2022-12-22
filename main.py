from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    """Home Page: The Landing Page of the app"""
    return "<p>This is the Home Page</p>"


@app.route("/signup", methods=['GET'])
def signup():
    """Send the user to Globus Auth with signup=1."""
    return "<p>This is the Sign Up Page</p>"


@app.route("/login", methods=['GET'])
def login():
    """Send the user to Globus Auth."""
    return "<p>Log In Page"


if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
