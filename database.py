import sqlite3

mydb = sqlite3.connect('blogging.sqlite', check_same_thread=False)
cursor = mydb.cursor()


def create_blog(user_id, username, title, desc, images_one=''):
    success = True
    try:
        query = 'INSERT INTO blogs (user_id, username, title, description, image_path_one) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(query, (user_id, username, title, desc, images_one))
        mydb.commit()
        msg = 'Successfully Added Blog'
    except sqlite3.IntegrityError:
        success = False
        mydb.rollback()
        msg = 'Blog Title already exist, please change title.'
    except Exception as exe:
        success = True
        mydb.rollback()
        print(exe)
        msg = 'Error occurred while creating blogging. Please contact Admin'
    return success, msg


def update_blog(blog_id, title, description):
    success = True
    try:
        query = f"UPDATE blogs SET title='{title}', description='{description}' WHERE blog_id='{blog_id}'"
        cursor.execute(query)
        mydb.commit()
        msg = 'Successfully Update Blogs'
    except sqlite3.IntegrityError:
        success = False
        msg = 'Blog Title already present, please change title.'
        mydb.rollback()
    except Exception as exe:
        success = False
        mydb.rollback()
        print(exe)
        msg = 'Error occurred while Update blogging. Please contact Admin'
    return success, msg


def fetch_blog():
    try:
        query = 'select * from blogs'
        cursor.execute(query)
        result = cursor.fetchall()
        # result = result* 40
        return True, result
    except Exception as exe:
        print(exe)
        msg = 'Error occurred while fetching all blogging. Please contact Admin'
        return False, msg


def create_user(username, email, password):
    try:
        success = True
        query = 'INSERT INTO user (username, email, password) VALUES (?, ?, ?)'
        cursor.execute(query, (username, email, password))
        mydb.commit()
        msg = 'User Added successfully'
    except sqlite3.IntegrityError:
        success = False
        msg = f'User with email {email} is already present.'
    except Exception as exe:
        success = False
        print(exe)
        msg = 'Error occurred while creating user. Please Contact Admin.'
    return success, msg


def check_user(email, password):
    try:
        query = 'Select user_id, username FROM user WHERE email=? and password=?'
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        if len(result) > 0:
            return True, result
        else:
            msg = 'Invalid credential. Please check again'
            return False, msg
    except Exception as exe:
        print(exe)
        msg = 'Error occurred while fetching user blogging. Please contact Admin'
        return False, msg
