from flask import Flask, render_template, redirect, request, url_for, session, flash
import globus_sdk
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Unique client id registered with Globus
CLIENT_ID = "d1802d87-57ab-4373-b475-5a73478936ea"

# Authentication Client
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
    """Renders the 2-step Login Flow"""
    return render_template('login.html')
    # return "<p>This is the Sign Up Page</p>"


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    """Send the user to Globus Auth"""

    if request.method == 'GET':
        # Step 1. Generate the Native App Authorization Token
        authorize_url = client.oauth2_get_authorize_url()
        return redirect(authorize_url)

    elif request.method == 'POST':
        # Step 2: Validate the Authorization Token, and Generate the Access Token
        auth_code = request.form["auth_code"]
        try:
            token_response = client.oauth2_exchange_code_for_tokens(auth_code)
        except globus_sdk.services.auth.errors.AuthAPIError:
            return redirect(url_for("error",
                                    error_name="Authorization Key Mismatch",
                                    error_desc="Please follow the instructions in the login page and try again."
                                    ))

        id_token = token_response.decode_id_token()

        # Store the login info in Session
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
    """Render the Profile page after successful authentication"""

    # If no user is logged in redirect to homepage
    if 'primary_identity' not in session.keys():
        flash("Error: Unauthorized Access")
        return redirect(url_for("error",
                                error_name="Unauthorized Access",
                                error_desc="Sorry, you need to login first!"))

    # If the user's user_id matches with the authenticated user_id show the profile
    elif session['primary_identity'] == user_id:
        return render_template("profile.html", session=session)

    # Otherwise redirect to homepage
    else:
        return redirect(url_for("error",
                                error_name="Unauthorized Access",
                                error_desc="Sorry, you need to login first!"))


@app.route("/logout", methods=['GET'])
def logout():
    """Logout, and remove Access Tokens"""
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    
    # Revoke the tokens
    if 'tokens' in session.keys():
        for token_info in session["tokens"].values():
            for token in token_info["access_token"]:
                client.oauth2_revoke_token(token)

    # Clear the session
    session.clear()

    redirect_uri = url_for("home", _external=True)
    globus_logout_uri = (
        "https://auth.globus.org/v2/web/logout"
        + "?client={}".format(CLIENT_ID)
        + "&redirect_uri={}".format(redirect_uri)
        + "&redirect_name=Authorization Portal"
    )

    return redirect(globus_logout_uri)


@app.route("/error/<error_name>/<error_desc>", methods=["GET"])
def error(error_name, error_desc):
    """Display Error"""
    return render_template("error.html", error_name=error_name, error_desc=error_desc)


if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
