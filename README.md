# Globus Auth Portal

A simple web-based application demonstrating how to build and execute the Globus Auth Services

## Getting Started
The Globus Sample Data Portal requires Python 3.9 or newer.

#### Create your own App registration for use in the Portal. 
* Visit the [Globus Developer Pages](https://developers.globus.org) to register an App.
* If this is your first time visiting the Developer Pages you'll be asked to create a Project. A Project is a way to group Apps together.
* When registering the App you'll be asked for some information, including the redirect URL and any scopes you will be requesting.
    * Redirect URL: `https://localhost:8080/authcallback` (note: if using EC2 `localhost` should be replaced with the IP address of your instance).
    * Scopes: `urn:globus:auth:scope:transfer.api.globus.org:all`, `openid`, `profile`, `email`
* After creating your App the client id can be copied into this project as `CLIENT_ID` 


### OS X

##### Environment Setup

* Install python3
* `git clone https://github.com/confusedDip/secret-data-portal.git`
* `cd secret-data-portal`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

##### Running the App

* `./main.py`
* point your browser to `https://localhost:8080`


### Linux (Ubuntu)

##### Environment Setup

* `sudo apt-get update`
* `sudo apt-get install python3-pip`
* `sudo pip install virtualenv`
* `sudo apt-get install git`
* `git clone https://github.com/confusedDip/secret-data-portal.git`
* `cd secret-data-portal`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

##### Running the App

* `./main.py`
* point your browser to `https://localhost:8080`


### Windows

##### Environment Setup

* Install Python3 (<https://www.python.org/downloads/windows/>)
* `pip install virtualenv`
* Install git (<https://git-scm.com/downloads>)
* `git clone https://github.com/confusedDip/secret-data-portal.git`
* `cd secret-data-portal`
* `virtualenv venv`
* `venv\Scripts\activate`
* `pip install -r requirements.txt`

##### Running the Portal App

* `python main.py`
* point your browser to `https://localhost:8080`
