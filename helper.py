import time

from flask import request, redirect, url_for, session
from functools import wraps
import re
import os


class ProjectException(Exception):
    def __init__(self, msg):
        self.msg = msg


def must_logged_in(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if session.get('id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return dec


def no_user_logging(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if session.get('id') is not None:
            return redirect(url_for('logout', next=request.url))
        return f(*args, **kwargs)

    return dec


def check_password(password):
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        raise ProjectException(msg='Password Length should be greater than 8')


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        raise ProjectException(msg='Invalid Email')


def check_title(title):
    if not str(title).isalpha():
        raise ProjectException(msg='Title can only have Alphabets')


def upload_images(request, key='img'):
    try:
        uploaded_file = request.files[key]
        if uploaded_file.filename != '':
            extension = uploaded_file.filename.split('.')[-1]
            filename = os.path.join('static', 'img', str(time.time())).replace('.', '_') + f'.{extension}'
            base_file = os.path.join(__file__.split('helper.py')[0], filename)
            f = open(base_file, 'w')
            f.close()
            uploaded_file.save(base_file)
            return filename
        else:
            return ''
    except Exception as ex:
        print(ex)
        BaseException('Enable to read image')
