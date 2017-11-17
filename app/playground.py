'''lansweeper-all

Usage:
  lansweeper-all -type <n>
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
    WITH pre_pivoted (TicketID, FieldID, FieldName, FieldData)
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
            IN (15, 52, 107)
        ORDER BY [TicketID],[FieldID]
    )
    SELECT DISTINCT TicketID AS TicketID, [Location of Issue], [Training Issues]
        FROM (
            SELECT DISTINCT TicketID, FieldName, FieldData
            FROM pre_pivoted
        ) x
        PIVOT (
            MAX(FieldData)
            FOR FieldName IN ("Location of Issue", "Training Issues")
        ) p
    ) y
"""


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


if __name__ == '__main__':
    execute_query("FieldNames", RAW_QUERY)
