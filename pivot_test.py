import records
import json
import pandas

# Log into the MS-SQL Server using a user-specified DSN.  I called mine
# "PSI-SQL-DSN"
server = "PSI-SQL-DSN"
db = records.Database(db_url="mssql://" + server)

# Write the query that gets all the FieldNames and FieldData for a given
# TicketID prior to pivoting
pivoted_query = """
    DECLARE @query  AS NVARCHAR(MAX)

    SET @query = '
        WITH pre_pivoted (TicketID, FieldID, FieldName, FieldData)
        AS (
            SELECT TOP 1000 htblticketcustomfield.ticketid as [TicketID],
                 htblticketcustomfield.fieldid as [FieldID],
                 htblcustomfields.name as [FieldName],
                 htblticketcustomfield.data as [FieldData]
            FROM [lansweeperdb].[dbo].[htblticketcustomfield]
            INNER JOIN htblcustomfields
              ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
            WHERE htblticketcustomfield.fieldid NOT IN (27,41,42,43,45,52,88)
            ORDER BY [TicketID],[FieldID]
        )
        SELECT * FROM pre_pivoted
        '
    EXEC(@query);
"""

print(db.query(pivoted_query).export("json"))
