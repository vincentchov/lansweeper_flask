
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
                IN (15,41,52,123)
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
            LIKE ''EH & S - Environmental Health & Safety''
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
            IN (15,41,52,123)
        ORDER BY [TicketID],[FieldID]
    )
    SELECT *
    FROM to_join
    LEFT JOIN (
    SELECT DISTINCT TicketID AS TicketID_2, ' + @cols + '
        FROM (
            SELECT TicketID, FieldName, FieldData
            FROM pre_pivoted
        ) x
        PIVOT (
            MAX(FieldData)
            FOR FieldName IN (' + @cols + ')
        ) p
    ) y
    ON y.TicketID_2 = to_join.TicketID
    '
    PRINT(@query)
