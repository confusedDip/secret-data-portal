from flask import Flask, render_template

app = Flask(__name__)

CLIENT_ID = "059ef9e1-0041-442d-9d24-ef354560bc2c"


@app.route("/", methods=['GET'])
def home():
    """Home Page: The Landing Page of the app"""
    return render_template('index.html')


@app.route("/signup", methods=['GET'])
def signup():
    """Send the user to Globus Auth with signup."""
    return "<p>This is the Sign Up Page</p>"


@app.route("/login", methods=['GET'])
def login():
    """Send the user to Globus Auth with login."""
    return "<p>Log In Page"


if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
