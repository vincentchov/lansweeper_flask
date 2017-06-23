import pyodbc, records, json
from secrets import sql_user, sql_passwd

# Log into the MS-SQL Server
# Connect to the MS-SQL Server using a user-specified DSN.  I called mine "PSI-SQL-DSN"
server = "PSI-SQL-DSN"
database = "lansweeperdb"
username = sql_user
password = sql_passwd
db = records.Database(db_url="mssql://{}:{}@{}".format(username, password, server))

# Get the custom field info for your ticket number
rows = db.query("SELECT * FROM htblticketcustomfield WHERE htblticketcustomfield.ticketid = 98;")
print(rows.dataset)
