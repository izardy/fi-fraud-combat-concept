from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

import requests
from datetime import datetime

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

bp = Blueprint('main', __name__)

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

import json

from flask import jsonify
@bp.route('/')
@login_required
def index():
    db = get_db()

    accountID=g.user['accountID']
    productNAME=g.user['productNAME']

    query_account_balance = "SELECT accountBAL FROM 'productID(1)-transactions'"+ " WHERE accountID = '"+ accountID + "' ORDER BY ROWID DESC LIMIT 1"
    query_last_5_transactions = "SELECT * FROM 'productID(1)-transactions'"+ " WHERE accountID = '"+ accountID + "' ORDER BY ROWID DESC LIMIT 5"
    query_total_monthly_transactions = """
    WITH RECURSIVE 
    dates(date) AS (
    SELECT date('now', 'start of month', '-11 months')
    UNION ALL
    SELECT date(date, '+1 month')
    FROM dates
    WHERE date < date('now', 'start of month')
    )
    SELECT 
    strftime('%Y-%m', dates.date) as month,
    COALESCE(SUM(CASE WHEN Amount < 0 THEN ABS(Amount) ELSE 0 END), 0) as total_expenses
    FROM dates
    LEFT JOIN "productID(1)-transactions" 
    ON strftime('%Y-%m', "productID(1)-transactions".date) = strftime('%Y-%m', dates.date)
    AND accountID = '"""+ accountID + """'
    GROUP BY strftime('%Y-%m', dates.date)
    ORDER BY month;
    """
    query_total_monthly_debit_transactions_by_category = """
    SELECT *, ROUND((total_amount/denominator)*100, 2) as pct FROM
    (SELECT *, SUM(ABS(total_amount)) OVER() as denominator FROM 
    (SELECT category, COUNT(*) as transaction_count, SUM(ABS(Amount)) as total_amount, ROUND(AVG(ABS(Amount)), 2) as average_amount
    FROM 
    (SELECT * FROM "productID(1)-transactions" WHERE accountID = '"""+ accountID + """' AND transactionTYPE = "Debit" AND date >= date('now', '-30 days') ORDER BY ROWID DESC)
    GROUP BY category))
        """
    
    account_balance = db.execute(
        query_account_balance
    ).fetchone()

    # Handle case where no transactions exist
    balance = account_balance['accountBAL'] if account_balance else 0

    last_5_transactions = db.execute(
        query_last_5_transactions
    ).fetchall()

    last_5_transactions_json = []
    for transaction in last_5_transactions:
            transaction_dict = dict(
            date=transaction['date'],
            description=transaction['description'],
            type=transaction['transactionTYPE'],
            amount=float(transaction['Amount']),  # Ensure amount is float
            status=transaction['status'])
            
            last_5_transactions_json.append(transaction_dict)

    last_5_transactions_json = json.dumps(last_5_transactions_json)

    total_monthly_transactions = db.execute(
        query_total_monthly_transactions
    ).fetchall()

    months_list = []
    total_monthly_transactions_list = []
    for transaction in total_monthly_transactions:
            month=transaction['month']
            total_expenses=float(transaction['total_expenses'])
            months_list.append(month)
            total_monthly_transactions_list.append(total_expenses)

    months_list_update = []
    for month in months_list:
         if '-01' in month:
             #month = month.replace("-01", " Jan")
             month = "Jan"
             months_list_update.append(month)
         elif '-02' in month:
             #month = month.replace("-02", " Feb")
             month = "Feb"
             months_list_update.append(month)
         elif '-03' in month:
             #month = month.replace("-03", " Mar")
             month = "Mar"
             months_list_update.append(month)
         elif '-04' in month:
             #month = month.replace("-04", " Apr")
             month = "Apr"
             months_list_update.append(month)
         elif '-05' in month:
             #month = month.replace("-05", " May")
             month = "May"
             months_list_update.append(month)
         elif '-06' in month:
             #month = month.replace("-06", " Jun")
             month = "Jun"
             months_list_update.append(month)
         elif '-07' in month:
             #month = month.replace("-07", " Jul")
             month = "Jul"
             months_list_update.append(month)
         elif '-08' in month:
             #month = month.replace("-08", " Aug")
             month = "Aug"
             months_list_update.append(month)
         elif '-09' in month:
             #month = month.replace("-09", " Sep")
             month = "Sep"
             months_list_update.append(month)
         elif '-10' in month:
             #month = month.replace("-10", " Oct")
             month = "Oct"
             months_list_update.append(month)
         elif '-11' in month:
             #month = month.replace("-11", " Nov")
             month = "Nov"
             months_list_update.append(month)
         elif '-12' in month:
             #month = month.replace("-12", " Dec")
             month = "Dec"
             months_list_update.append(month)

    months_list_update =  ','.join(months_list_update)

    
    
    total_monthly_debit_transactions_by_category = db.execute(query_total_monthly_debit_transactions_by_category).fetchall()
    category_list = []
    pct_category_list = []
    for category_transaction in total_monthly_debit_transactions_by_category:
            category=category_transaction['category']
            pct_category=float(category_transaction['pct'])
            category_list.append(category)
            pct_category_list.append(pct_category)

    category_list = list(set([x for x in category_list if x is not None]))

    category_list =  ','.join(category_list)

        

    return render_template('app/index.html', account_balance=balance, productNAME=productNAME, 
                            accountID=accountID, last_5_transactions_json=last_5_transactions_json,
                            months_list_update=months_list_update,  total_monthly_transactions_list=total_monthly_transactions_list,
                            category_list=category_list, pct_category_list=pct_category_list)

#################################################################################### [ADD SCAMMER]

@bp.route('/add_scammer', methods=['POST', 'GET'])
@login_required
def add_scammer():

    # Get user ID
    reporterID = g.user['id']

    # Get current datetime in format compatible with datetime-local
    recordedDate = datetime.now().strftime("%Y-%m-%dT%H:%M")

    if request.method == 'POST':
        scammerName = request.form['scammer_name']
        contact = request.form['contact_info']
        reportedDate = request.form['reported_date']
        bankAccount = request.form['bank_account']
        bankName = request.form['bank_name']
        bankAccountName = request.form['bank_account_name']
    

        platform = request.form['platform']

        tiktokID = request.form['tiktok']
        facebookID = request.form['facebook']
        twitterID = request.form['twitter']
        instagramID = request.form['instagram']
        telegramID = request.form['telegram']
        sourceReport1 = request.form['url_1']
        sourceReport2 = request.form['url_2']
        sourceReport3 = request.form['url_3']

        db = get_db()
        db.execute(
            """
            INSERT INTO scammer (scammerName, contact, reporterID, reportedDate, recordedDate, bankAccount, bankName, bankAccountName, 
            platform, tiktokID, facebookID, twitterID, instagramID, telegramID, sourceReport1, sourceReport2, sourceReport3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (scammerName, contact, reporterID, reportedDate, recordedDate, bankAccount, bankName, bankAccountName, platform, tiktokID, facebookID, twitterID, instagramID, telegramID, sourceReport1, sourceReport2, sourceReport3)
        )
        db.commit()
    
    return render_template('app/add-scammer.html')

#################################################################################### [FIND SCAMMER]

@bp.route('/search_scammer', methods=['POST', 'GET'])
@login_required
def search_scammer():    
    return render_template('app/search-scammer.html')

#################################################################################### [MANAGE SCAMMER - USER]

# [SHOW CONTRIBUTED LIST]
@bp.route('/manage_scammer_user', methods=['POST', 'GET'])
@login_required
def manage_scammer_user():
    db = get_db()
    scammers = db.execute(
        'SELECT * FROM scammer WHERE reporterID='+str(g.user['id'])
    ).fetchall()
    
    return render_template('app/manage-scammer.html', scammers=scammers)

# [EDIT CONTRIBUTED LIST]

def get_scammer(id):
    scammer = get_db().execute(
        'SELECT *'
        ' FROM scammer'
        ' WHERE scammerID = ?',(id,)
    ).fetchone()

    if scammer is None:
        abort(404, f"Scammer id {id} doesn't exist.")

    return scammer

# [UPDATE/EDIT INFO]

@bp.route('/<int:id>/scammer_update', methods=('POST', 'GET'))
@login_required
def scammer_update(id):
    db = get_db()
    scammer_update = get_scammer(id)

    # Fetch comments for this scammer id
    comments = db.execute(
        'SELECT user_id, content, created_at FROM comments WHERE post_id = ? ORDER BY created_at DESC',
        (id,)
    ).fetchall()

    if request.method == 'POST':
        scammerName = request.form['scammer_name']
        contact = request.form['contact_info']
        reportedDate = request.form['reported_date']
        bankAccount = request.form['bank_account']
        bankName = request.form['bank_name']
        bankAccountName = request.form['bank_account_name']
    
        platform = request.form['platform']
        tiktokID = request.form['tiktok']
        facebookID = request.form['facebook']
        twitterID = request.form['twitter']
        instagramID = request.form['instagram']
        telegramID = request.form['telegram']
        
        sourceReport1 = request.form['url_1']
        sourceReport2 = request.form['url_2']
        sourceReport3 = request.form['url_3']

        user_id = g.user['username']
        new_comment = request.form['new_comment']

        error = None

        if not scammerName:
            error = '!'
        if not contact:
            error = '!'
        if not reportedDate:
            error = '!'
        if not bankAccount:
            error = '!'
        if not bankName:
            error = '!'
        if not bankAccountName:
            error = '!'

        if not platform:
            error = '!'
        if not tiktokID:
            error = '!'
        if not facebookID:
            error = '!'
        if not twitterID:
            error = '!'
        if not instagramID:
            error = '!'
        if not telegramID:
            error = '!'

        elif not sourceReport1:
            error = '!'

        if error is not None:
            flash(error)
        
        else:

            # Get current datetime in format compatible with datetime-local
            recordedDate = datetime.now().strftime("%Y-%m-%dT%H:%M")
            
            # Update scammer info
            db.execute(
                'UPDATE scammer SET scammerName = ?, contact = ?, reportedDate = ?, recordedDate = ?, bankAccount = ?, bankName = ?, bankAccountName = ?, platform = ?, tiktokID = ?, facebookID = ?,'
                'twitterID = ?, instagramID = ?, telegramID = ?, sourceReport1 = ?, sourceReport2 = ?, sourceReport3 = ?'
                ' WHERE scammerID = ?',
                (scammerName, contact, reportedDate, recordedDate, bankAccount, bankName, bankAccountName, platform, tiktokID, facebookID, twitterID, instagramID, telegramID, sourceReport1, sourceReport2, sourceReport3, id)
            )

            # Insert new comment if provided
            if new_comment:
                db.execute(
                    'INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)',
                    (id, user_id, new_comment)
                )

            db.commit()
            return redirect(url_for('main.manage_scammer'))

    return render_template('app/scammer-update.html', scammer_update=scammer_update, comments=comments)


#################################################################################### [MANAGE SCAMMER - ADMIN]


@bp.route('/manage_scammer_admin', methods=['POST', 'GET'])
@login_required
def manage_scammer_admin():
    if g.user['username']=='izardyamir@gmail.com':
        db = get_db()
        scammers = db.execute(
            'SELECT * FROM scammer'
        ).fetchall()
        
        return render_template('app/manage-scammer.html', scammers=scammers)

@bp.route('/<int:id>/admin_update', methods=('GET', 'POST'))
def admin_update(id):
    if g.user['username']=='izardyamir@gmail.com':
        db = get_db()

        # Fetch user
        users = db.execute(
            'SELECT * FROM cif WHERE id = ?',
            (id,)
        ).fetchone()

        if request.method == 'POST':
        
            email = request.form['email']
            phone = request.form['phone']
            address1 = request.form['address1']
            address2 = request.form['address2']
            postcode = request.form['postcode']
            area = request.form['area']
            state = request.form['state']
            error = None
            
            if not email:
                error = 'email is required.'

            if not phone:
                error = 'phone is required.'

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
                    'UPDATE cif SET email = ?, phone = ?, address1 = ?, address2 = ?, postcode = ?, area = ?, state = ?'
                    ' WHERE id = ?',
                    (email, phone, address1, address2, postcode, area, state, id)
                )
                db.commit()
                return redirect(url_for('auth.registered_users'))

    return render_template('auth/admin-update.html', users=users)

#################################################################################### [SCAMMER SEARCH]

@bp.route('/search_scammer', methods=('GET', 'POST'))
@login_required

def search_scammer():

    db = get_db()
    properties = db.execute(
        'SELECT *'
        ' FROM scammer'
        #' ORDER BY id ASC'
    ).fetchall()


    if request.method == 'POST':
        scammerName =request.form['search_by_name']
        bankAccount =request.form['search_by_acc_no']
        contact =request.form['search_by_contact_info']
        facebookID =request.form['search_by_facebook_id']
        tiktokID =request.form['search_by_tiktok_id']
        twitterID =request.form['search_by_twitter_id']
        instagramID =request.form['search_by_instagram_id']
        telegramID =request.form['search_by_telegram_id']
        platform ='%'+(request.form['search_by_platform'])+'%'

        error = None

        if not scammerName:
            scammerName = ''
        if not bankAccount:
            bankAccount = ''
        if not contact:
            contact = ''
        if not facebookID:
            facebookID = ''
        if not tiktokID:
            tiktokID = ''
        if not twitterID:
            twitterID = ''
        if not instagramID:
            instagramID = ''
        if not telegramID:
            telegramID = ''
        if not platform:
            platform = ''
        if error is not None:
            flash(error)                
        else:
            db = get_db()
            properties = db.execute(
                'SELECT id,property_name,property_status,property_address,stateInput,districtInput,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,phone'
                ' FROM property'
                 ' WHERE (stateInput = ? OR districtInput = ? OR property_name like :property_name) AND (ttl_room = ? OR ttl_bathroom = ? OR aircond = ? OR wifi = ? OR washing = ? OR cooking = ?) AND (homestay_rate <= ?)',(stateInput,districtInput,property_name,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,)
                #' ORDER BY id ASC'
            ).fetchall()
            return render_template('dashboard/search_property_guest.html', properties=properties)
    
    return render_template('dashboard/search_property_guest.html', properties=properties)
                


#################################################################################### [TRANSFER]

@bp.route('/transfer', methods=['POST', 'GET'])
@login_required
def transfer():    
    return render_template('app/transfer.html')

#################################################################################### [MANAGE]
'''
@bp.route('/')
@login_required
def index():
    return render_template('app/index.html')
'''
