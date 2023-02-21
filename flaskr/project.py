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


@bp.route("/chicago-crimes/introduction", methods=['GET', 'POST'])
def chicago_crimes_introduction():
    return render_template('project/chicago-crimes/introduction.html')


@bp.route("/chicago-crimes/analysis", methods=['GET', 'POST'])
def chicago_crimes_analysis():
    return render_template('project/chicago-crimes/analysis.html')


@bp.route("/chicago-crimes/map", methods=['GET', 'POST'])
def chicago_crimes_map():
    return render_template('project/chicago-crimes/map.html')
