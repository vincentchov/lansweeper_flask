'''lansweeper-all

Usage:
  lansweeper-all -type <n>
  lansweeper-all count (--tickets | --defects)
  lansweeper-all -h | --help
  lansweeper-all --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Report Types:
     Option | Report Type
    =================================================
        0   | Administrative / Business Development
        1   | Customer / Vendor Related
        2   | EH & S - Environmental Health & Safety
        3   | Engineering
        4   | Export Compliance
        5   | Facility / Maintenance
        6   | Human Resources
        7   | IT Support
        8   | Project Management / Management Issues
        9   | Purchasing & Accounting
        10  | Quality
        11  | Security
        12  | Shop Operations
        13  | Timesheet System
        14  | Training
'''
import records
import json
import pyodbc
import pathlib
from docopt import docopt

# Set up the database
if __name__ == '__main__':
    from constants import SQL_FRAGMENTS
    from secrets import get_sql_uri
    MS_SQL_URI = get_sql_uri()
    db = records.Database(db_url=MS_SQL_URI)
else:
    from .constants import SQL_FRAGMENTS
    from .secrets import get_sql_uri
    from app import db

__version__ = "0.1.0"
__author__ = "Vincent Chov"
__license__ = "MIT"


# Write the query that gets all the FieldNames and FieldData for a given
# TicketID prior to pivoting
RAW_QUERY = """
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


def get_report_types():
    report_types = [(key, item['typename'])
                    for key, item in SQL_FRAGMENTS.items()]
    return report_types


def get_report_types_prompt():
    report_types = get_report_types()
    prompt = "Choose an option by entering the associated number:\n"
    for i, report_type in enumerate(report_types):
        report_type_name = report_type[1]
        prompt += "{}: {}\n".format(i, report_type_name)
    return prompt


def interactive_query():
    prompt = get_report_types_prompt()
    while True:
        print(prompt)
        try:
            option = int(input(prompt))
            execute_report_given_option(arg)
        except ValueError:
            print("Invalid input. Choose a number from the list of options...")
            continue


def format_query(report_type, query):
    # Generate a query based on the report type the user chose
    return query.format(SQL_FRAGMENTS[report_type]['fieldid'],
                        SQL_FRAGMENTS[report_type]['to_join'],
                        SQL_FRAGMENTS[report_type]['select'],
                        SQL_FRAGMENTS[report_type]['join'],
                        SQL_FRAGMENTS[report_type]['typename'],
                        SQL_FRAGMENTS[report_type]['group_by'],
                        SQL_FRAGMENTS[report_type]['fieldid'])


def execute_query(report_type, query):
    # The filename's output is the lowercase form of the report name
    dest_folder = "Reports"
    pathlib.Path(dest_folder).mkdir(parents=True, exist_ok=True)
    filename = report_type.lower()
    full_path = '{}/{}.xlsx'.format(dest_folder, filename)
    results = db.query(query)
    with open(full_path, 'wb') as f:
        f.write(results.export('xlsx'))
        f.close()

    print("Done!")
    return (filename + '.xlsx', results)


def execute_report_given_option(option):
    """
        Takes the option as an int, validate the input and then performs the
        query.
    """
    if 0 <= option <= 14:
        report_types = get_report_types()
        report_type = report_types[option][0]
        final_query = format_query(report_type, RAW_QUERY)
        filename, results = execute_query(report_type, final_query)
    else:
        error_str = "The option selected must be an integer between 0 and 14."
        raise ValueError(error_str)

    return (filename, results)


def count_by_ticket_types():
    # Get report types to query against
    query = """
        SELECT TOP 10000
            htblticket.ticketid as TicketID,
            htbltickettypes.typename as TicketType
        FROM htblticket
        INNER JOIN htbltickettypes
            ON htblticket.tickettypeid = htbltickettypes.tickettypeid
        ORDER BY htblticket.ticketid DESC
    """
    filename, results = execute_query("ticket_count", query)
    # Convert results to Pandas DataFrame to count up ticket types
    df = results.export('df')
    counted = df.groupby('TicketType').count()
    print(counted)
    return counted


def main():
    """ Main entry point for the lansweeper-all CLI. """
    args = docopt(__doc__, version=__version__)
    if args['<n>']:
        try:
            arg = int(args['<n>'])
            filename, results = execute_report_given_option(arg)
        except ValueError as e:
            exit("The option selected must be an integer between 0 and 14.")
    elif args['count'] and args['--tickets']:
        print("User chose to count ticket types.")
        count_by_ticket_types()
    elif args['count'] and args['--defects']:
        print("User chose to count defects")
    else:
        print("Invalid input.")


if __name__ == '__main__':
    main()
