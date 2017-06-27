import pyodbc, records, json, pandas
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

pre_pivoted_query = "SELECT TOP (1000) htblticketcustomfield.ticketid as [TicketID], htblticketcustomfield.fieldid as [FieldID], htblcustomfields.name as [FieldName], htblticketcustomfield.data as [FieldData] FROM [lansweeperdb].[dbo].[htblticketcustomfield] INNER JOIN htblcustomfields ON htblticketcustomfield.fieldid = htblcustomfields.fieldid WHERE [lansweeperdb].[dbo].[htblticketcustomfield].fieldid NOT IN (27,41,42,43,45,52,88) ORDER BY [TicketID],[FieldID];"

df_to_pivot = pandas.read_json(db.query(pre_pivoted_query).export("json"))
pivoted = pandas.pivot_table(df_to_pivot, index=['TicketID'], columns=['FieldName'], aggfunc=lambda x: ' '.join(x))

to_join_query = "SELECT DISTINCT htblticket.ticketid as TicketID,htbltickettypes.typename as TicketType,tblassets.AssetName as AssetName,tsysAssetTypes.AssetTypename as AssetTypeName FROM [lansweeperdb].[dbo].[htblticket] INNER JOIN htblticketcustomfield ON htblticket.ticketid = htblticketcustomfield.ticketid INNER JOIN htblcustomfields ON htblticketcustomfield.fieldid = htblcustomfields.fieldid INNER JOIN tblassets ON htblticket.assetid = tblassets.assetid INNER JOIN tsysAssetTypes ON tblassets.AssetType = tsysAssetTypes.AssetType INNER JOIN htbltickettypes ON htblticket.tickettypeid = htbltickettypes.tickettypeid WHERE htbltickettypes.typename LIKE 'IT Support' AND htblticketcustomfield.FieldID IN (55, 60, 72, 81, 83, 84, 85, 89, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 103) ORDER BY htblticket.ticketid;"

df_to_join = pandas.read_json(db.query(to_join_query).export("json"))

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
