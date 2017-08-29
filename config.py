from secrets import PSI_DB_HOST, AWS_HOST, AWS_USER, AWS_PASS
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
WSGI_APPLICATION = 'app.wsgi.application'

if os.name == 'posix':
    MS_SQL_URI = "mssql://{}:{}@{}".format(AWS_USER,
                                           AWS_PASS,
                                           AWS_HOST)
else:
    server = PSI_DB_HOST
    MS_SQL_URI = "mssql://{}".format(PSI_DB_HOST)
