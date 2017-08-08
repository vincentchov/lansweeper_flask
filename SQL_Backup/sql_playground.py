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


my_query = """
    SELECT * FROM htblticket WHERE htblticket.ticketid = 208
"""

with open('my_file.csv', 'w') as my_file:
    my_file.write(db.query(my_query).export("csv"))
