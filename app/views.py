from app import app, db
from flask import redirect, flash, request, url_for, jsonify, render_template
from config import *
import json

@app.route('/')
def index():
    return "Hello world!"
