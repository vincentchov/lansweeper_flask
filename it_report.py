import pyodbc, records, json
from secrets import sql_user, sql_passwd

# Log into the MS-SQL Server
# Connect to the MS-SQL Server using a user-specified DSN.  I called mine "PSI-SQL-DSN"
server = "PSI-SQL-DSN"
database = "lansweeperdb"
username = sql_user
password = sql_passwd
db = records.Database(db_url="mssql://{}:{}@{}".format(username, password, server))

def queryAndPrintDataSet(queryString):
    rows = db.query(queryString)
    print(rows.dataset)

def queryAndPrintJSON(queryString):
    rows = db.query(queryString)
    print(json.dumps(json.loads(rows.export('json')), indent=4, sort_keys=True))

# Example: Get the custom field info for your ticket number
queryAndPrintDataSet("SELECT * FROM htblticketcustomfield WHERE htblticketcustomfield.ticketid = 98;")
