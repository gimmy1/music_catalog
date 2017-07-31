from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask import url_for
from flask import flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from database_setup import Category
from database_setup import CategoryItem
from database_setup import User
# from database_setup import User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

''' JSON '''


@app.route('/itemcatalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/itemcatalog/<int:catalog_id>/items/JSON')
def categoryItemJSON(catalog_id):
    categoryItems = session.query(CategoryItem).filter_by(
        category_id=catalog_id).all()
    return jsonify(categoryItems=[categoryItem.serialize for categoryItem in categoryItems])

''' END OF JSON '''

''' LOGIN '''


@app.route('/login')
def login():
    # create a state token to prevent request forgery
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    # store it in session for later use
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print request.args.get('state'), login_session['state']
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print '401'
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    # print credentials
    # return credentials

    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('allCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('allCategories'))


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

''' END OF LOGOUT '''

# route displays only Categories


@app.route('/')
@app.route('/itemcatalog/')
def allCategories():
    categories = session.query(Category).all()
    return render_template('allcategories.html', categories=categories)


# route is responsible for showing all items of targeted category
@app.route('/itemcatalog/<int:catalog_id>/')
@app.route('/itemcatalog/<int:catalog_id>/items/')
def categoryItems(catalog_id):
    # Prevent unwanted request to server
    # catch only if catalog exists otherwise a user can submit requests through the browser even if
    # id does not exists. AVOID HIGH SECURITY RISKS.
    try:
        categories = session.query(Category).all()
        category = session.query(Category).filter_by(id=catalog_id).first()

        categoryName = category.name
        categoryItems = session.query(CategoryItem).filter_by(
            category_id=catalog_id).all()

        return render_template('categoryItems.html', categories=categories,
                               categoryItems=categoryItems, categoryName=categoryName)
    except:
        return redirect(url_for('allCategories'))


# route is responsible for routing user to description url
@app.route('/itemcatalog/<int:catalog_id>/items/<int:item_id>/')
def itemDescription(catalog_id, item_id):
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    item_owner = getUserInfo(categoryItem.user_id)

    return render_template('itemDescription.html', categoryItem=categoryItem, item_owner=item_owner)

''' CRUD FUNCTIONALITY '''


@app.route('/itemcatalog/new/', methods=['GET', 'POST'])
def newItem():
    # return 'new item added'
    # categoryItem = session.query(CategoryItem).filter_by(id=item_id)
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == "POST":
        if not request.form['name'] or not request.form['description']:
            flash("Name and Description are required")
            return redirect(url_for('newItem'))

        newItem = CategoryItem(name=request.form['name'], description=request.form['description'],
                               category_id=request.form['category'], user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("You have successfully created a new item!")

        return redirect(url_for('allCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('newItem.html', categories=categories)
    # categoryItem = session.query(CategoryItem).filter_by(id=item.id).


@app.route('/itemcatalog/<int:catalog_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(catalog_id, item_id):
    # return 'edit item'
    if 'username' not in login_session:
        return redirect('login')

    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()
    item_owner = getUserInfo(categoryItem.user_id)

    if item_owner.id != login_session['user_id']:
        return redirect('/allCategories')

    categories = session.query(Category).all()

    if request.method == "POST":
        if request.form['name']:
            categoryItem.name = request.form['name']
        if request.form['description']:
            categoryItem.description = request.form['description']
        if request.form['category']:
            categoryItem.category_id = request.form['category']
        session.add(categoryItem)
        session.commit()
        flash("You have successfully edited this item.")
        return redirect(url_for('itemDescription', catalog_id=categoryItem.category_id, item_id=categoryItem.id))
    else:
        return render_template('editItem.html', categories=categories, categoryItem=categoryItem)


@app.route('/itemcatalog/<int:catalog_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(catalog_id, item_id):
    # return 'delete the damn item?!'
    if 'username' not in login_session:
        return redirect('/login')

    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()
    item_owner = getUserInfo(categoryItem.user_id)

    if item_owner.id != login_session['user_id']:
        return redirect('/allCategories')

    if request.method == "POST":
        session.delete(categoryItem)
        session.commit()
        flash("You have successfully deleted the item.")
        return redirect(url_for('categoryItems', catalog_id=categoryItem.category_id, item_id=categoryItem.id))
    else:
        return render_template('deleteItem.html', categoryItem=categoryItem)

''' END OF CRUD '''

if __name__ == '__main__':
    app.secret_key = "secret key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
