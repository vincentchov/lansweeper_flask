import json
from config import *
from app import app, db
from sqlalchemy.exc import ResourceClosedError
from .lansweeper_all import execute_report_given_option
from flask import redirect, flash, request, url_for, jsonify, render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reports/<option_int>')
def reports(option_int):
    try:
        option_int = int(option_int)
        execute_report_given_option(option_int)
        message = "Success!"
    except ValueError as e:
        message = str(e)
    except ResourceClosedError as e:
        message = "No tickets found!"

    context_dict = {'message': message}
    return render_template('reports.html', context=context_dict)
