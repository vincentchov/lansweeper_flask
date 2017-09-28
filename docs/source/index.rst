.. Lansweeper documentation master file, created by
   sphinx-quickstart on Thu Sep 28 14:27:12 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Getting reports for a new TicketType in Lansweeper
==================================================

“Simple” overview as to how writing a report works (get a cup of coffee first)
------------------------------------------------------------------------------
In order to obtain reports, one needs to write a SQL script that runs on the Microsoft SQL Server that Lansweeper communicates with to store tickets as well as what kind of information a given ticket type can store (Location, Time, etc).  SQL stands for “Structured Query Language”, which is a language used to search for information as well as update information in a SQL database.  A SQL database is essentially a much more efficient alternative to Excel for storing tabular data.  

For any given ticket, there are types of information (or columns) that are common among all tickets, regardless of if they’re an “IT Support” ticket, “Customer / Vendor Related”, etc.  This information is stored in the following tables: “htblticket”, “htbltickettypes”, “OriginUser”, “htblticketstates”, “htblsource”, “AgentUser”, and “htblnotes”.  Basic information on a given ticket is in the “htblticket” table, which contains information that help get information from all the other tables.  Together, they can be used to create a report containing the columns (TicketID, TicketType, State, [Creation Date], [Originator Name], Source, [Agent Name], [Time Worked (Minutes), [Date of Last Update]]).  Those columns are columns that all ticket types can have.  So far, so good.

My reporting script first generates a table with all of those columns.  From there, it generates another table that contains columns that only certain ticket types can have, like what kind of hardware is having problems in an IT Support ticket (if applicable).  This is where things get a little complicated.  The problem is that the table generated in the previous paragraph is built-into Lansweeper where there are specific columns you can search against.  For the more specific columns, these columns are custom fields, that is custom columns that we’ve told Lansweeper are available.  All information for these custom columns is stored in the following tables: “htblticketcustomfield” and “htblcustomfields”.  

For a given ticket, the report’s second table contains the columns (TicketID, FieldID, FieldName, FieldData).  There will be multiple rows of information for a given ticket, for each custom column name (FieldName), as well as the actual value for the custom column (FieldData).  For example, just for the custom column “Hardware”, which says what hardware is affected in an “IT Support” ticket, there will be a row like (1, 26, “Hardware”, “Laptop”).  So there will be a row of that form for each custom column that a ticket has.  There could be a dozen or more rows just to cover all the different columns that are specific to a given ticket type.

In order to join the two tables together to make one big table, the second table needs to convert the rows to columns, such that the values for FieldName becomes a column, and the same thing for FieldData.  We will need to do what is called a pivot table, which requires us to know ahead of time what all the column names can be and say that you want those columns.  When the custom column names are finalized, that can be done.  It will be tedious, but straightforward.  However, since the column names haven’t been finalized, I wrote what’s called a dynamic SQL script that searches for all the column names first, dynamically write a query with all of those column names, and then performs the query.  It’s code that writes other code.  

Once the second table is done being pivoted from rows to columns, we can finally join it with the first table and call it a day.

More specific action steps 
--------------------------
	The first thing you’ll want to do is to find out the names of all of the fields/columns you want in the report as well as the name of the ticket type you want a report for.  From there, you’ll want to search the htblticketcustomfield table for all rows with the field names you want in the report.  Note down the FieldIDs for each field name.  Now we start filling in the placeholders in my SQL script.  The following is my SQL script with the placeholders in it

.. code-block:: python

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
                        IN {0}
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
            WITH to_join (TicketID, TicketType, {1}State,
                          [Creation Date], [Originator Name], Source, [Agent Name],
                          [Time Worked (Minutes)], [Date of Last Update])
            AS (
                SELECT DISTINCT TOP 10000
                    htblticket.ticketid as TicketID,
                    htbltickettypes.typename as TicketType,
                    {2}htblticketstates.statename AS State,
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
                {3}INNER JOIN htbltickettypes
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
                    LIKE ''{4}''
                GROUP BY htblticket.ticketid,
                    htbltickettypes.typename,
                    {5}htblticketstates.statename,
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
                    IN {6}
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

1. Copy and paste them as a comma-separated tuple into my SQL script where it says {6}.
2. Copy and paste the ticket type’s name into {4}.
3. The following only applies if it’s an IT Support ticket.  Type in everything manually, without the quotes and also include any newlines.
4. Replace {0} with the same tuple from {6}.  Replace {1} with ::

    Asset Name, AssetTypeName, 

5. Replace {2} with ::

    tblassets.AssetName as AssetName,
    tsysAssetTypes.AssetTypename as AssetTypeName,

6. Replace {3} with ::
 
    INNER JOIN tblassets
        ON htblticket.assetid = tblassets.assetid
    INNER JOIN tsysAssetTypes
        ON tblassets.AssetType = tsysAssetTypes.AssetType

7. Replace {5} with ::

    tblassets.AssetName,
    tsysAssetTypes.AssetTypename,



