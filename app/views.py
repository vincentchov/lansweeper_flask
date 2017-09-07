from app import app, db
from .lansweeper_all import execute_report_given_option
from flask import redirect, flash, request, url_for, jsonify, render_template
from config import *
import json


@app.route('/')
def index():
    return "Hello world!"


@app.route('/reports/<option_int>')
def reports(option_int):
    try:
        option_int = int(option_int)
        execute_report_given_option(option_int)
        return "Success!"
    except ValueError as e:
        return str(e)
