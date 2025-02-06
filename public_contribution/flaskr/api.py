from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/scammers', methods=['GET'])
@login_required
def get_scammers():
    try:
        db = get_db()
        scammers = db.execute('SELECT * FROM scammer').fetchall()
        
        # Convert the sqlite rows to a list of dictionaries
        scammer_list = []
        for scammer in scammers:
            scammer_dict = {
                'scammerID': scammer['scammerID'],
                'scammerName': scammer['scammerName'],
                'phone': scammer['phone'],
                'reporterID': scammer['reporterID'],
                'reportedDate': scammer['reportedDate'],
                'recordedDate': scammer['recordedDate'],
                'bankAccount': scammer['bankAccount'],
                'bankName': scammer['bankName'],
                'bankAccountName': scammer['bankAccountName'],
                'email': scammer['email'],
                'tiktokID': scammer['tiktokID'],
                'facebookID': scammer['facebookID'],
                'twitterID': scammer['twitterID'],
                'instagramID': scammer['instagramID'],
                'telegramID': scammer['telegramID'],
                'sourceReport1': scammer['sourceReport1'],
                'sourceReport2': scammer['sourceReport2'],
                'sourceReport3': scammer['sourceReport3']
            }
            scammer_list.append(scammer_dict)

        return jsonify({
            'success': True,
            'data': scammer_list
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500