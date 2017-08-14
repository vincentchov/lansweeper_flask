import records
import json
import pandas
import os


# Log into the MS-SQL Server using a user-specified DSN.  I called mine
# "PSI-SQL-DSN"
if os.name == 'posix':
    from secrets import sql_user, sql_passwd
    server = "AWS-SQL"
    username = sql_user
    password = sql_passwd
    db = records.Database(db_url="mssql://{}:{}@{}".format(username,
                                                           password,
                                                           server))
else:
    server = "PSI-SQL-DSN"
    db = records.Database(db_url="mssql://" + server)


query = """
    SELECT * FROM htblticketcustomfield
    INNER JOIN htblcustomfields
        ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
"""
filename = os.path.basename(__file__).replace('.py', '')
with open('../Reports/{}.xls'.format(filename), 'wb') as f:
    f.write(db.query(query).export('xls'))
