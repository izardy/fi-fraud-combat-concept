from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

import requests

from werkzeug.exceptions import abort

from cryptography.fernet import Fernet

from flaskr.auth import login_required
from flaskr.db import get_db

from flask_paginate import Pagination, get_page_args

import functools

from IPython.display import HTML
import pandas as pd
import numpy as np
import os


#################################################################################### [LOAD USER ID]

bp = Blueprint('app', __name__)

def load_logged_in_user():
        
    user_id = session.get('user_id')
        
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
    uploaded_file_path_pdf = "flaskr/static/data/"+ str(g.user['id'])+"/pdf/"
        
    try:
        uploaded_file=os.listdir(uploaded_file_path_pdf)[0]
        if ".pdf" in uploaded_file:
            os.remove(uploaded_file_path_pdf+uploaded_file)
    except:
        uploaded_file=None

#################################################################################### [LOGIN CHECK]

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#################################################################################### [PAGE MAIN]

@bp.route('/')
@login_required
def index():
    return render_template('app/index.html')

