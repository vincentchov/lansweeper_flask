import json
from config import *
from app import app, db
from sqlalchemy.exc import ResourceClosedError
from .lansweeper_all import execute_report_given_option, get_report_types
from flask import redirect, flash, request, url_for, jsonify, render_template


@app.route('/')
def index():
    report_types = get_report_types()
    indexed_report_types = []
    for i, report_pair in enumerate(report_types):
        indexed_report_types.append((i, report_pair[1]))

    context_dict = {'report_types': indexed_report_types}
    return render_template('index.html', context=context_dict)


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
