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
    print("\n")

def queryAndPrintJSON(queryString):
    rows = db.query(queryString)
    print(json.dumps(json.loads(rows.export('json')), indent=4, sort_keys=True))
    print("\n")

# # Example: Use a ticket number to match ticketcustomfield's field data with their field name
# rows = db.query("SELECT * FROM htblticketcustomfield WHERE htblticketcustomfield.ticketid = 100 ORDER BY htblticketcustomfield.fieldid;")
# field_ids = []
# # Get the field ids
# for row in rows:
#     field_ids.append(row.fieldid)
#
# for field_id in field_ids:
#     queryAndPrintDataSet("SELECT * FROM htblcustomfields WHERE htblcustomfields.fieldid = {};".format(field_id))
#     other_rows = db.query("SELECT * FROM htblticketcustomfield WHERE htblticketcustomfield.ticketid = 100 AND htblticketcustomfield.fieldid = {};".format(field_id))
#     print(other_rows.dataset, "\n\n\n============================================================================================================================= \n")

# queryAndPrintDataSet("SELECT ticketid,assetid,tickettypeid FROM htblticket WHERE htblticket.ticketid = 100;")
