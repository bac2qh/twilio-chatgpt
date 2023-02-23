import functools

from flask import (
    Blueprint, flash, current_app, g, redirect, render_template, request, Flask, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


import os
import openai

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
        print('no message received')

    if body:
        out = chatgpt_send_message(body)['choices'][0]['text']
        db.execute(
            "INSERT INTO sms (body, sender_number, receiver_number) VALUES (?,?,?)",
            (out, 'ChatGPT', from_)
        )
        db.commit()
        # f"ChatGPT response to {from_}: {out}"
    return 'message logged'


@bp.route("/sms/received", methods=['GET', 'POST'])
def SMS_received(sender_number=None):
    if request.method == 'POST':
        sender_number = request.form['sender_number']
        if sender_number != None:
            db = get_db()
            Q = db.execute(
                'SELECT * from sms WHERE sender_number = ?'
                'ORDER BY created DESC LIMIT 1',
                (sender_number, )
            ).fetchone()
            A = db.execute('SELECT * from sms WHERE sender_number="ChatGPT"'
                           ' and receiver_number = ?'
                           ' ORDER BY created DESC LIMIT 1',
                           (sender_number, )
                           ).fetchone()
            return render_template('api/sms/received.html', Q=Q, A=A)
    return render_template('api/sms/received.html', Q=None, A=None)


def chatgpt_send_message(message):

    openai.api_key = current_app.config['OPENAI_API_KEY']

    out = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=100,
        temperature=0
    )

    return out
