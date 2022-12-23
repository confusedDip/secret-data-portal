from flask import Flask, render_template, redirect, request, url_for, session, flash
import globus_sdk
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

CLIENT_ID = "d1802d87-57ab-4373-b475-5a73478936ea"

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(refresh_tokens=True)


@app.route("/", methods=['GET'])
def home():
    """Home Page: The Landing Page of the app"""
    # Check whether already some user is logged in
    if 'primary_identity' in session.keys():
        if session['is_authenticated']:
            return redirect(url_for('profile', user_id=session['primary_identity']))

    # Otherwise:
    return render_template('index.html')


@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')
    # return "<p>This is the Sign Up Page</p>"


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    """Send the user to Globus Auth with signup."""

    if request.method == 'GET':

        authorize_url = client.oauth2_get_authorize_url()
        return redirect(authorize_url)

    elif request.method == 'POST':
        auth_code = request.form["auth_code"]
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)

        id_token = token_response.decode_id_token()

        session.update(
            tokens=token_response.by_resource_server,
            is_authenticated=True,
            name=id_token.get('name'),
            email=id_token.get('email'),
            institution=id_token.get('organization'),
            primary_username=id_token.get('preferred_username'),
            primary_identity=id_token.get('sub'),
        )
        return redirect(url_for('profile', user_id=session['primary_identity']))


@app.route("/profile/<user_id>", methods=['GET'])
def profile(user_id):
    if 'primary_identity' not in session.keys():
        flash("Error: Unauthorized Access")
        return redirect(url_for("home"))

    elif session['primary_identity'] == user_id:
        return render_template("profile.html", session=session)

    else:
        flash("Error: Unauthorized Access")
        return redirect(url_for("home"))


@app.route("/logout", methods=['GET'])
def logout():
    # Revoke the tokens
    if 'tokens' in session.keys():
        for token_info in session["tokens"].values():
            for token in token_info["access_token"]:
                client.oauth2_revoke_token(token)

    # Clear the session
    session.clear()

    # Redirect to Home
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
