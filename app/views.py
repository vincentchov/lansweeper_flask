import json
import tempfile
import pandas as pd
import xlsxwriter
from config import *
from app import app, db
from io import BytesIO
import flask_excel as excel
from sqlalchemy.exc import ResourceClosedError
from .lansweeper_all import execute_report_given_option, get_report_types
from flask import (redirect, flash, request, url_for,
                   jsonify, render_template, send_file, send_from_directory)


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
        filename, results = execute_report_given_option(option_int)
        df = results.export('df')
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, 'Sheet1')
        writer.close()
        output.seek(0)
        excel.init_excel(app)
        return send_file(output,
                         as_attachment=True,
                         attachment_filename=filename)
    except ValueError as e:
        message = str(e)
    except ResourceClosedError as e:
        message = "No tickets found!"

    context_dict = {'message': message}
    return render_template('reports.html', context=context_dict)
