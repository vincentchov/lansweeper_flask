from flask import Flask
import records
import pyodbc

app = Flask(__name__)
app.config.from_object('config')
db = records.Database(db_url=app.config['MS_SQL_URI'])

from app import views
