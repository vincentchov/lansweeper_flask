import os
from app.secrets import get_sql_uri

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
WSGI_APPLICATION = 'app.wsgi.application'

MS_SQL_URI = get_sql_uri()
