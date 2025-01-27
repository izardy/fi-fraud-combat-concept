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

@bp.route('/register', methods=('GET', 'POST'))  # Changed endpoint
def register():
    if request.method == 'POST':
        # Get form data from CORRECT fields
        email = request.form['register-username']
        password = request.form['register-password']
        confirm_password = request.form['confirm-register-password']
        
        # Add password confirmation check
        if password != confirm_password:
            error = 'Passwords do not match'
            flash(error)
            return redirect(url_for('auth.register'))

        # Set default values for other fields
        defaults = {
            'username': email,  # Using email as username
            'firstname': '-',
            'lastname': '-',
            'gender': '-',
            'dob': '-',
            'address1': '-',
            'address2': '-',
            'postcode': '-',
            'area': '-',
            'state': '-'
        }

        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # Corrected SQL with proper columns/values
                db.execute(
                    """INSERT INTO cif 
                    (username, password, firstname, lastname, gender, dob,
                     address1, address2, postcode, area, state) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (email, generate_password_hash(password),
                     defaults['firstname'], defaults['lastname'], defaults['gender'], defaults['dob'],
                     defaults['address1'], defaults['address2'], defaults['postcode'],
                     defaults['area'], defaults['state'])
                )
                db.commit()
            except db.IntegrityError:
                error = f"Email {email} is already registered."
            else:
                flash('Registration successful. Please log in.')
                return redirect(url_for('auth.login'))

        flash(error)
        return redirect(url_for('auth.register'))

    return render_template('auth/login.html')


####################################################################################

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # Match the form field names from your HTML
        email = request.form['login-username']  # Changed from username
        password = request.form['login-password']
        
        db = get_db()
        error = None
        cif = db.execute(
            'SELECT * FROM cif WHERE username = ?', (email,)  # Changed to email
        ).fetchone()

        if cif is None:
            error = 'Incorrect username.'
        elif not check_password_hash(cif['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = cif['id']
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
            'SELECT * FROM cif WHERE id = ?', (user_id,)
        ).fetchone()
                
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
