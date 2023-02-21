import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, Flask, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from twilio.twiml.messaging_response import MessagingResponse

bp = Blueprint('project', __name__, url_prefix='/project')


@bp.route("/twilio-chatgpt", methods=['GET', 'POST'])
def twilio_chatgpt():
    return render_template('project/twilio-chatgpt.html')
