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
                FROM htblticketcustomfield
                INNER JOIN htblcustomfields
                    ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
                WHERE htblticketcustomfield.fieldid
                    IN (45,43,15,55,56,58,57,88,60,104,105,
                        83,85,100,103,101,102,84,90,89)
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
        WITH to_join (TicketID, TicketType, AssetName, AssetTypeName, State,
                      [Creation Date], [Originator Name], Source, [Agent Name],
                      [Time Worked (Minutes)], [Date of Last Update])
        AS (
            SELECT DISTINCT TOP 10000
                htblticket.ticketid as TicketID,
                htbltickettypes.typename as TicketType,
                tblassets.AssetName as AssetName,
                tsysAssetTypes.AssetTypename as AssetTypeName,
                htblticketstates.statename AS State,
                htblticket.date AS [Creation Date],
                OriginUser.name AS [Originator Name],
                htblsource.name AS Source,
                AgentUser.name AS [Agent Name],
                SUM(htblnotes.timeworked) AS [Time Worked (Minutes)],
                htblticket.updated AS [Date of Last Update]
            FROM htblticket
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
            INNER JOIN htblticketstates
                ON htblticketstates.ticketstateid = htblticket.ticketstateid
            INNER JOIN htblusers AS OriginUser
                ON OriginUser.userid = htblticket.fromuserid
            INNER JOIN htblsource
                ON htblsource.sourceid = htblticket.sourceid
            LEFT JOIN htblagents
                ON htblagents.agentid = htblticket.agentid
            LEFT JOIN htblusers AS AgentUser
                ON AgentUser.userid = htblagents.userid
            LEFT JOIN htblnotes
                ON htblnotes.ticketid = htblticket.ticketid
            WHERE htbltickettypes.typename
                LIKE ''IT Support''
            GROUP BY htblticket.ticketid,
                htbltickettypes.typename,
                tblassets.AssetName,
                tsysAssetTypes.AssetTypename,
                htblticketstates.statename,
                htblticket.date,
                OriginUser.name,
                htblsource.name,
                AgentUser.name,
                htblticket.updated
             ORDER BY htblticket.ticketid
        ),
        pre_pivoted (TicketID, FieldID, FieldName, FieldData)
        AS (
            SELECT TOP 10000
                htblticketcustomfield.ticketid as [TicketID],
                htblticketcustomfield.fieldid as [FieldID],
                htblcustomfields.name as [FieldName],
                htblticketcustomfield.data as [FieldData]
            FROM htblticketcustomfield
            INNER JOIN htblcustomfields
                ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
            WHERE htblticketcustomfield.fieldid
                IN (45,43,15,55,56,58,57,88,60,104,105,
                    83,85,100,103,101,102,84,90,89)
            ORDER BY [TicketID],[FieldID]
        )
        SELECT *
        FROM to_join
        LEFT JOIN (
        SELECT DISTINCT TicketID AS TicketID, ' + @cols + '
            FROM (
                SELECT TicketID, FieldName, FieldData
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
with open('Reports/{}.xlsx'.format(filename), 'wb') as f:
    f.write(db.query(pivoted_query).export('xlsx'))
