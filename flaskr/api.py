import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, Flask, session, url_for
)
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from twilio.twiml.messaging_response import MessagingResponse

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/sms/receive", methods=['GET', 'POST'])
def SMS_receive():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    from_ = request.values.get('From', None)
    to_ = request.values.get('To', None)

    error = None

    db = get_db()
    try:
        db.execute(
            "INSERT INTO sms (body, sender_number, receiver_number) VALUES (?,?,?)",
            (body, from_, to_)
        )
        db.commit()
    except:
        raise Exception("Error inserting into sms table")

    print(body)
    print(from_)
    print(to_)

    # resp = MessagingResponse()
    # # Add a message
    # resp.message("message received")
    return render_template('api/sms/receive.html')


@bp.route("/sms/received", methods=['GET', 'POST'])
def SMS_received():
    db = get_db()
    latest_message = db.execute(
        'SELECT * from sms ORDER BY created DESC LIMIT 1'
    ).fetchone()

    return render_template('api/sms/received.html', latest_message=latest_message)