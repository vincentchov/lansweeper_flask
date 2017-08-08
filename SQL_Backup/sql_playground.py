import records
import json
import pandas
import os


server = "PSI-SQL-DSN"
db = records.Database(db_url="mssql://" + server)

db.query("""
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
        LIKE 'IT Support' AND htblticketcustomfield.FieldID IN
        (15, 55, 60, 72, 81, 83, 84, 85, 89, 90, 91, 92, 93,
         94, 95, 96, 97, 100, 101, 103)
    ORDER BY htblticket.ticketid
""")
