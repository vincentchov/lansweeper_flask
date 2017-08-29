USE [lansweeperdb]
GO

DECLARE @my_cols AS NVARCHAR(MAX),
		@query  AS NVARCHAR(MAX),
		@fieldids AS NVARCHAR(MAX) = '15, 106',
		@typename AS NVARCHAR(MAX) = 'Export Compliance';

WITH cols(col_string)
AS (
	SELECT [lansweeperdb].[dbo].[get_lansweeper_cols](@fieldids, @typename)
) 
SELECT @my_cols = cols.col_string FROM cols;

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
                LIKE ''' + @typename + '''
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
                IN (SELECT * FROM [dbo].cast_csv_ints(''' + @fieldids + '''))
            ORDER BY [TicketID],[FieldID]
        )
        SELECT *
        FROM to_join
        LEFT JOIN (
        SELECT DISTINCT TicketID AS TicketID, ' + @my_cols + '
            FROM (
                SELECT TicketID, FieldName, FieldData
                FROM pre_pivoted
            ) x
            PIVOT (
                MAX(FieldData)
                FOR FieldName IN (' + @my_cols + ')
            ) p
        ) y
        ON y.TicketID = to_join.TicketID
        '
        EXEC(@query);