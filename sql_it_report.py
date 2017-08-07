import records
import json
import pandas

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
                WHERE htblticketcustomfield.fieldid
                    NOT IN (27,41,42,43,45,52,88)
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
        WITH to_join (TicketID, FieldID, FieldName, FieldData)
        AS (
            SELECT DISTINCT TOP 10000
                htblticket.ticketid as TicketID,
                htbltickettypes.typename as TicketType,
                tblassets.AssetName as AssetName,
                tsysAssetTypes.AssetTypename as AssetTypeName
             FROM [lansweeperdb].[dbo].[htblticket]
             INNER JOIN htblticketcustomfield
                ON htblticket.ticketid = htblticketcustomfield.ticketid
             INNER JOIN htblcustomfields
                ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
             INNER JOIN tblassets
                ON htblticket.assetid = tblassets.assetid
             INNER JOIN tsysAssetTypes
                ON tblassets.AssetType = tsysAssetTypes.AssetType
             INNER JOIN htbltickettypes
                ON htblticket.tickettypeid = htbltickettypes.tickettypeid
             WHERE htbltickettypes.typename
                LIKE ''IT Support'' AND htblticketcustomfield.FieldID IN
                (15, 55, 60, 72, 81, 83, 84, 85, 89, 90, 91, 92, 93,
                 94, 95, 96, 97, 100, 101, 103)
             ORDER BY htblticket.ticketid
        ),
        pre_pivoted (TicketID, FieldID, FieldName, FieldData)
        AS (
            SELECT TOP 10000
                htblticketcustomfield.ticketid as [TicketID],
                htblticketcustomfield.fieldid as [FieldID],
                htblcustomfields.name as [FieldName],
                htblticketcustomfield.data as [FieldData]
            FROM [lansweeperdb].[dbo].[htblticketcustomfield]
            INNER JOIN htblcustomfields
                ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
            WHERE htblticketcustomfield.fieldid NOT IN (27,41,42,43,45,52,88)
            ORDER BY [TicketID],[FieldID]
        )
        SELECT * FROM to_join
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

with open('it_report.xls', 'wb') as f:
    f.write(db.query(pivoted_query).export('xls'))
