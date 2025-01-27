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

#################################################################################### [USER REGISTRATION]

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


#################################################################################### [PASSWORD VERFICATION STATE]

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

#################################################################################### [LOGGED IN USER]

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM cif WHERE id = ?', (user_id,)
        ).fetchone()

#################################################################################### [LIST USER]

@bp.route('/registered_users')
@login_required
def registered_users():
    if g.user['username']=='izardyamir@gmail.com':
        db = get_db()
        users = db.execute(
            'SELECT *'
            ' FROM cif'
        ).fetchall()
        return render_template('app/registered_users.html', users=users)
    else:
        return redirect(url_for('index'))

#################################################################################### [UPDATE USER PROFILE (ADMIN)]

@bp.route('/<int:id>/admin_update', methods=('GET', 'POST'))
@login_required
def admin_update(id):
    if g.user['username']=='izardyamir@gmail.com':
        db = get_db()

        # Fetch user
        users = db.execute(
            'SELECT * FROM cif WHERE id = ?',
            (id,)
        ).fetchone()

        if request.method == 'POST':
        
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            gender = request.form['gender']
            dob = request.form['dob']
            ic = request.form['ic']
            email = request.form['email']
            address1 = request.form['address1']
            address2 = request.form['address2']
            postcode = request.form['postcode']
            area = request.form['area']
            state = request.form['state']
            error = None
            
            if not firstname:
                error = 'firstname is required.'

            if not lastname:
                error = 'lastname is required.'
            
            if not gender:
                error = 'gender is required.'

            if not dob:
                error = 'dob is required.'

            if not ic:
                error = 'ic is required.'

            if not email:
                error = 'email is required.'

            if not address1:
                error = 'address1 is required.'

            if not address2:
                error = 'address2 is required.'

            if not postcode:
                error = 'postcode is required.'

            if not area:
                error = 'area is required.'

            if not state:
                error = 'state is required.'

            if error is not None:
                flash(error)

            else:
                db = get_db()
                db.execute(
                    'UPDATE cif SET firstname = ?, lastname = ?, gender = ?, dob = ?, ic = ?, email = ?, address1 = ?, address2 = ?, postcode = ?, area = ?, state = ?'
                    ' WHERE id = ?',
                    (firstname, lastname, gender, dob, ic, email, address1, address2, postcode, area, state, id)
                )
                db.commit()
                return redirect(url_for('registered_users'))

    return render_template('auth/admin-update.html', users=users)
                
#################################################################################### [USER LOGOUT]

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
