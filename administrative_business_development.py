import records
import json
import pandas
import os

if os.name == 'posix':
    server = "AWS-SQL"
    username = sql_user
    password = sql_passwd
    db = records.Database(db_url="mssql://{}:{}@{}".format(username,
                                                           password,
                                                           server))
else:
    server = "PSI-SQL-DSN"
    db = records.Database(db_url="mssql://" + server)


# Write the query that gets all the FieldNames and FieldData for a given
# TicketID prior to pivoting
pivoted_query = """
    DECLARE @cols AS NVARCHAR(MAX),
            @query  AS NVARCHAR(MAX)

    SELECT @cols =  STUFF((
        SELECT DISTINCT ',' + QUOTENAME(FieldName)
        FROM (
            SELECT DISTINCT TicketID, FieldData, FieldName
            FROM (
                SELECT TOP 1000 htblticketcustomfield.ticketid as [TicketID],
                    htblticketcustomfield.fieldid as [FieldID],
                    htblcustomfields.name as [FieldName],
                    htblticketcustomfield.data as [FieldData]
                FROM [lansweeperdb].[dbo].[htblticketcustomfield]
                INNER JOIN htblcustomfields
                    ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
                WHERE htblticketcustomfield.fieldid IN (154,155,156)
                ORDER BY [TicketID],[FieldID]
            ) y
         ) x
         GROUP BY FieldName, TicketID
         FOR XML
            PATH(''),
            TYPE
         ).value('.', 'NVARCHAR(MAX)'),
         1,
         1,
         ''
    )

    SET @query = '
        WITH to_join (TicketID, TicketType)
        AS (
            SELECT DISTINCT TOP 10000
                htblticket.ticketid as TicketID,
                htbltickettypes.typename as TicketType
             FROM [lansweeperdb].[dbo].[htblticket]
             INNER JOIN htblticketcustomfield
                ON htblticket.ticketid = htblticketcustomfield.ticketid
             INNER JOIN htblcustomfields
                ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
             INNER JOIN htbltickettypes
                ON htblticket.tickettypeid = htbltickettypes.tickettypeid
             WHERE htbltickettypes.typename
                LIKE ''Administrative / Business Development''
             ORDER BY htblticket.ticketid
        ),
        pre_pivoted (TicketID, FieldID, FieldName, FieldData)
        AS (
            SELECT TOP 1000
                htblticketcustomfield.ticketid as [TicketID],
                htblticketcustomfield.fieldid as [FieldID],
                htblcustomfields.name as [FieldName],
                htblticketcustomfield.data as [FieldData]
            FROM [lansweeperdb].[dbo].[htblticketcustomfield]
            INNER JOIN htblcustomfields
                ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
            WHERE htblticketcustomfield.fieldid IN (154,155,156)
            ORDER BY [TicketID],[FieldID]
        )
        SELECT y.TicketID, TicketType, ' + @cols + '
        FROM to_join
        LEFT JOIN (
        SELECT DISTINCT TicketID AS TicketID, ' +
            @cols + '
            FROM (
                SELECT TicketID, FieldData, FieldName
                FROM pre_pivoted
            ) x
            PIVOT (
                MAX(FieldData)
                FOR FieldName IN (' + @cols + ')
            ) p
        ) y
        ON y.TicketID = to_join.TicketID
        '
    EXEC(@query);
"""
filename = os.path.basename(__file__).replace('.py', '')
with open('Reports/{}.xls'.format(filename), 'wb') as f:
    f.write(db.query(pivoted_query).export('xls'))
