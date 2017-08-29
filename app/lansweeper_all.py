import records
import json
import pandas
import os
from constants import SQL_FRAGMENTS

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
query = """
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
"""

# Form list of report types and prompt the user to choose one
report_types = [(key, item['typename']) for key, item in SQL_FRAGMENTS.items()]
prompt = "Choose an option: \n"
for i, report_type in enumerate(report_types):
    report_type_name = report_type[1]
    prompt += "{}: {}\n".format(i, report_type_name)
while True:
    try:
        option = int(input(prompt))
        report_type = report_types[option][0]
    except ValueError:
        print("Invalid input.  Choose a number from the list of options...")
        continue
    else:
        # Done getting input
        print("Please wait...")
        break

# Generate a query based on the report type the user chose
exec("""formatted_query = query.format(SQL_FRAGMENTS['{0}']['fieldid'],
                                       SQL_FRAGMENTS['{0}']['to_join'],
                                       SQL_FRAGMENTS['{0}']['select'],
                                       SQL_FRAGMENTS['{0}']['join'],
                                       SQL_FRAGMENTS['{0}']['typename'],
                                       SQL_FRAGMENTS['{0}']['group_by'],
                                       SQL_FRAGMENTS['{0}']['fieldid'])
""".format(report_type))

# The filename's output is the lowercase form of the report name
filename = report_type.lower()
with open('Reports/{}.xlsx'.format(filename), 'wb') as f:
    f.write(db.query(formatted_query).export('xlsx'))
    f.close()

print("Done!")
