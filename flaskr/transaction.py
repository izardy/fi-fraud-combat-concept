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


#################################################################################### [MANAGE]
'''
@bp.route('/')
@login_required
def index():
    return render_template('app/index.html')
'''
