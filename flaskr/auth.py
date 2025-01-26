import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

import pandas as pd
from datetime import datetime

from flaskr.db import get_db
from flask import send_from_directory
from flask_login import LoginManager
login_manager = LoginManager()

bp = Blueprint('auth', __name__, url_prefix='/auth')

####################################################################################

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = 'male'
        dob = request.form['dob']
        username = request.form['username']
        password = request.form['password']
        worker_id = '-'  # assuming this should be a string
        locationSelect = '-'  # assuming this should be a string
        divisionSelect = '-'  # assuming this should be a string
        departmentSelect = '-'  # assuming this should be a string
        
        address1 = '-' 
        address2 = '-' 
        address3 = '-' 

        db = get_db()
        error = None

        if not firstname:
            error = 'First Name is required.'
        elif not lastname:
            error = 'Last Name is required.'
        elif not gender:
            error = 'Gender is required.'
        elif not dob:
            error = 'Date of birth is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, firstname, lastname, gender, dob, worker_id, locationSelect, divisionSelect, departmentSelect, address1, address2, address3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), firstname, lastname, gender, dob, worker_id, locationSelect, divisionSelect, departmentSelect, address1, address2, address3),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash('Registration successful. Please log in.')
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


####################################################################################

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

####################################################################################

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
                
#################################################################################### [SHOW USER INFO]

@bp.route('/user_view')
def list_info():
    db = get_db()
    user = db.execute(
        'SELECT id, username, firstname, lastname, gender,dob, worker_id,locationSelect, divisionSelect, departmentSelect, address1, address2, address3'
        ' FROM user'
        ' WHERE username = ?',(g.user['username'],)
        #' ORDER BY id ASC'
    ).fetchone()
    
    # Define the two dates
    date1_str = user['dob']
    date2_str = datetime.now().strftime("%Y-%m-%d")  # Get today's date
    
    # Convert strings to datetime objects
    date1 = datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")
    
    # Calculate the age
    age = int(abs(date2 - date1).days / 365.25)
    
    # transactions
    transactions = db.execute('SELECT * FROM transactions WHERE account_id = ? ORDER BY id DESC LIMIT 1',(g.user['id'],)).fetchone()
    
    return render_template('auth/user_view.html',user=user ,age=age, transactions=transactions)


####################################################################################

@bp.route('/<int:id>/user_update', methods=('GET', 'POST'))
def user_update(id):
    user = get_user(id)
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        locationSelect = request.form['locationSelect']
        divisionSelect = request.form['divisionSelect']
        departmentSelect = request.form['departmentSelect']
        
        address1 = request.form['stateSelect']
        address2 = request.form['districtSelect']
        address3 = request.form['areaSelect']
        
        
        error = None

        if not old_password:
            error = 'Password is required.'
        
        if not check_password_hash(g.user['password'], old_password):
            error = 'Incorrect password.'

        if not new_password:
            error = 'Password is required.'
        
        if not locationSelect:
            error = 'Location is required.'

        if not divisionSelect:
            error = 'Division is required.'
        
        if not departmentSelect:
            error = 'Department name is required.'
        
        if not address1:
            error = 'Address 1 is required.'

        if not address2:
            error = 'Address 2 is required.'
        
        if not address3:
            error = 'Address3 is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE user SET password = ?, locationSelect = ?, divisionSelect = ?, departmentSelect = ?, address1 = ?, address2 = ?, address3 = ?'
                ' WHERE id = ?',
                (generate_password_hash(new_password), locationSelect, divisionSelect, departmentSelect, address1, address2, address3, id)
            )
            db.commit()
            return redirect(url_for('index'))
        
    # Define the two dates
    date1_str = user['dob']
    date2_str = datetime.now().strftime("%Y-%m-%d")  # Get today's date
    
    # Convert strings to datetime objects
    date1 = datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")
    
    # Calculate the age
    age = int(abs(date2 - date1).days / 365.25)

    return render_template('auth/user_update.html', user=user, age=age)

#################################################################################### [SHOW USER TRANSACTION]

####################################################################################

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
