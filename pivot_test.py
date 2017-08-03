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
    DECLARE @cols AS NVARCHAR(MAX),
            @query  AS NVARCHAR(MAX)

    SELECT @cols = STUFF((SELECT DISTINCT ',' + QUOTENAME(FieldName)
                             FROM (SELECT DISTINCT TicketID
                                  , FieldData
                                  , FieldName
                                  FROM PrePivotTempTable
                                  ) x
                             GROUP BY FieldName, TicketID
                             FOR XML PATH(''),
                                        TYPE)
                            .value('.', 'NVARCHAR(MAX)'
                         ) ,1,1,'')

    SET @query = 'SELECT DISTINCT TicketID AS TicketID, ' + @cols +
                 ' FROM (
                       SELECT TicketID, FieldData, FieldName
                       FROM PrePivotTempTable
                   ) x
                   PIVOT
                   (
                       MAX(FieldData)
                       FOR FieldName IN (' + @cols + ')
                   ) p
                 '
    EXEC(@query);
"""

print(db.query(pivoted_query).export("json"))
