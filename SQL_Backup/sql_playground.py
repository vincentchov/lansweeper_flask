import records
import json
import pandas
import os
import tablib

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
    SELECT TOP 10000
        htblticketcustomfield.ticketid as [TicketID],
        htblticketcustomfield.fieldid as [FieldID],
        htblcustomfields.name as [FieldName],
        htblticketcustomfield.data as [FieldData]
    FROM [lansweeperdb].[dbo].[htblticketcustomfield]
    INNER JOIN htblcustomfields
        ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
    WHERE htblticketcustomfield.fieldid
        IN (15,107) AND htblticketcustomfield.ticketid = 257
    ORDER BY [TicketID],[FieldID]
"""
filename = os.path.basename(__file__).replace('.py', '')
results = db.query(query)
with open('../Reports/{}.xlsx'.format(filename), 'wb') as f:
    f.write(results.export('xlsx'))
