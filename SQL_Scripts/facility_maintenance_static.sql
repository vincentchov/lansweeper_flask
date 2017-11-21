
WITH to_join (TicketID, TicketType, State,
              [Creation Date], [Originator Name], Source, [Agent Name],
              [Time Worked (Minutes)], [Date of Last Update])
AS (
    SELECT DISTINCT TOP 10000
        htblticket.ticketid as TicketID,
        htbltickettypes.typename as TicketType,
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
        LIKE 'Facility / Maintenance Issues'
    GROUP BY htblticket.ticketid,
        htbltickettypes.typename,
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
                    (15,41,42,43,45,48,62,63,64,65,66,
                     67,68,69,72,73,74,75,76,78,80,142)

    ORDER BY [TicketID],[FieldID]
)
SELECT *
FROM to_join
LEFT JOIN (
SELECT DISTINCT TicketID AS TicketID_2, [Ceiling],[Facility Issue Types],[Has the issue been addressed or fixed?],[How many people are affected by the issue?],[Location of Issue],[Occurrence],[This could be a safety risk]
    FROM (
        SELECT TicketID, FieldName, FieldData
        FROM pre_pivoted
    ) x
    PIVOT (
        MAX(FieldData)
        FOR FieldName IN ([Ceiling],[Facility Issue Types],[Has the issue been addressed or fixed?],[How many people are affected by the issue?],[Location of Issue],[Occurrence],[This could be a safety risk])
    ) p
) y
ON y.TicketID_2 = to_join.TicketID
