from flask import Flask, render_template, request, redirect, url_for, session, abort
from functools import wraps
from database import *
from helper import *

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config["SESSION_PERMANENT"] = False
app.static_folder = 'static'


# to register new user [Done]
@app.route('/register', methods=['GET', 'POST'])
@no_user_logging
def register():
    if request.method == 'POST':
        try:
            user_name = request.form['username']
            password = request.form['password']
            email = request.form['email']
            check_email(email)
            check_password(password)
            success, msg = create_user(username=user_name, email=email, password=password)
            if not success:
                return render_template('register.html', msg=msg, session=session)
            else:
                return render_template('login.html', msg=msg, session=session)
        except Exception as ex:
            if isinstance(ex, ProjectException):
                msg = ex.msg
            else:
                msg = 'Invalid value in form, Please check again.<br>1.Email should be Unique.<br>2.Password should be 8 letter minimum and contain only letter and numbers.'
        return render_template('register.html', msg=msg, session=session)
    else:
        msg = '1.Email should be Unique.<br>2.Password should be 8 letter minimum and contain only letter and numbers.'
    return render_template('register.html', msg=msg, session=session)


# to login a user [Done]
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        success, output = check_user(email=email, password=password)
        if success:
            session['is_login'] = True
            session['id'] = output[0]
            session['username'] = output[1]
            session['blog_id'] = None
            msg = f'Welcome {output[1]}'
            return redirect(url_for('home'))
        else:
            session['is_login'] = False
            session['id'] = None
            return render_template('login.html', msg=output, session=session)
    else:
        msg = 'Please Fill the form'
    return render_template('login.html', msg=msg, session=session)


# logout current user [Done]
@app.route('/logout')
@must_logged_in
def logout():
    session['is_login'] = False
    session['id'] = None
    msg = 'Successfully logged out'
    return render_template('login.html', msg=msg, session=session)


# h
@app.route('/home', methods=['GET'])
@must_logged_in
def home():
    success, result = fetch_blog()
    if success:
        return render_template('home.html', result=result, session=session)
    else:
        return render_template('home.html', msg=result, result=[], session=session)


@app.route('/create', methods=['POST', 'GET'])
@must_logged_in
def create():
    if request.method == 'POST' and 'title' in request.form and 'description' in request.form:

        title = request.form['title']
        description = request.form['description']
        image_one = upload_images(request)
        success, msg = create_blog(user_id=session['id'], username= session['username'],  title=title, desc=description, images_one=image_one)
        if success:
            return redirect(url_for('home'))
        else:
            return render_template('create.html', msg=msg, session=session)
    else:
        msg = '- Please Fill the form <br>. - Title Should be Unique'
    return render_template('create.html', msg=msg, session=session)


@app.route('/update', methods=['POST', 'GET'])
@must_logged_in
def update():
    if request.method == 'POST':
        if 'title' in request.form and 'description' in request.form:
            title = request.form['title']
            description = request.form['description']
            success, msg = update_blog(blog_id=session['blog_id'], title=title, description=description)
            session['blog_id'] = None
            if success:
                return redirect(url_for('home'))
            else:
                return render_template('update.html', msg=msg, session=session)
        elif session['blog_id'] is None and 'update' in request.form:
            session['blog_id'] = int(request.form.get('update'))
            msg = f"Blog id to be update is {session['blog_id']}"
            return render_template('update.html', msg=msg, session=session)
        else:
            msg = 'Please Fill the form.<br>Title Should be Unique'
            return render_template('update.html', msg=msg, session=session)
    else:
        msg = 'Please Fill the form.<br>Title Should be Unique'
        return render_template('update.html', msg=msg, session=session)


if __name__ == '__main__':
    app.run(debug=True)
