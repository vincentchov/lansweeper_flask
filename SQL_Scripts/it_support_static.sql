
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
        LIKE 'IT Support'
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
     ORDER BY htblticket.ticketid DESC
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
        IN
            (15,43,45,52,55,56,57,58,60,82,83,84,85,
             88,89,90,91,92,93,94,95,96,97,98,99,100,
             101,102,103,104,105,157,158,159,160,168,
             175,177,178,179,180,181,182,183,184)

    ORDER BY [TicketID],[FieldID]
)
SELECT *
FROM to_join
LEFT JOIN (
SELECT DISTINCT TicketID AS TicketID_2, [Asset Ownership ],[Computer-Related Hardware],[Conference 1 - Projector part affected],[CSC Ticket Number],[CSC Ticket Submission Date],[Hardware Type],[Has the issue been addressed or fixed?],[How many people are affected by the issue?],[Laptop-related],[Location of Issue],[Network / Connection Issues],[Network / Connection Related],[PC / Tower - Related],[Pratt and Whitney UCA Asset Types],[Printing Hardware],[Printing Issues],[Projectors],[PSI Owned Asset Types],[Software ],[Software Issues],[Specific Defect],[Telecommunication Hardware],[Was this an Escape? (Min of 2 bus.days, +$5,000 loss, or Export Violation)]
    FROM (
        SELECT TicketID, FieldName, FieldData
        FROM pre_pivoted
    ) x
    PIVOT (
        MAX(FieldData)
        FOR FieldName IN ([Asset Ownership ],[Computer-Related Hardware],[Conference 1 - Projector part affected],[CSC Ticket Number],[CSC Ticket Submission Date],[Hardware Type],[Has the issue been addressed or fixed?],[How many people are affected by the issue?],[Laptop-related],[Location of Issue],[Network / Connection Issues],[Network / Connection Related],[PC / Tower - Related],[Pratt and Whitney UCA Asset Types],[Printing Hardware],[Printing Issues],[Projectors],[PSI Owned Asset Types],[Software ],[Software Issues],[Specific Defect],[Telecommunication Hardware],[Was this an Escape? (Min of 2 bus.days, +$5,000 loss, or Export Violation)])
    ) p
) y
ON y.TicketID_2 = to_join.TicketID
