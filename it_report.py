import pyodbc
import records
import json
import pandas
from secrets import sql_user, sql_passwd

# Log into the MS-SQL Server
# Connect to the MS-SQL Server using a user-specified DSN.  I called mine
# "PSI-SQL-DSN"

server = "PSI-SQL-DSN"
database = "lansweeperdb"
username = sql_user
password = sql_passwd
db = records.Database(db_url="mssql://{}:{}@{}".format(username,
                                                       password,
                                                       server))


def queryAndPrintDataSet(queryString):
    rows = db.query(queryString)
    print(rows.dataset)
    print("\n")


def queryAndPrintJSON(queryString):
    rows = db.query(queryString)
    print(json.dumps(json.loads(rows.export('json')),
                     indent=4, sort_keys=True), "\n")


# Write the query that gets all the FieldNames and FieldData for a given
# TicketID prior to pivoting
pre_pivoted_query = """
    SELECT htblticketcustomfield.ticketid as [TicketID],
           htblticketcustomfield.fieldid as [FieldID],
           htblcustomfields.name as [FieldName],
           htblticketcustomfield.data as [FieldData]
    FROM [lansweeperdb].[dbo].[htblticketcustomfield]
    INNER JOIN htblcustomfields
    ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
    WHERE [lansweeperdb].[dbo].[htblticketcustomfield].fieldid IN
        (15, 55, 60, 72, 81, 83, 84, 85, 89, 90, 91, 92, 93,
         94, 95, 96, 97, 100, 101, 103)
ORDER BY [TicketID],[FieldID];
"""

# Pivot and then drop the FieldName level in the DataFrame
df_to_pivot = pandas.read_json(db.query(pre_pivoted_query).export("json"))
pivoted = pandas.pivot_table(df_to_pivot,
                             index=['TicketID'],
                             columns=['FieldName'],
                             aggfunc=lambda x: ' '.join(x))
pivoted.columns = pivoted.columns.droplevel()

# Write the query that gets the other information for a given TicketID
to_join_query = """
    SELECT DISTINCT htblticket.ticketid as TicketID,
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
     ORDER BY htblticket.ticketid;
"""

# Perform the SQL query and store the results in a Pandas DataFrame
df_to_join = pandas.read_json(db.query(to_join_query).export("json"))

# Join the two DataFrames: pivoted and df_to_join
joined = df_to_join.join(pivoted, on="TicketID")

# Reorder the columns so the final table starts with the right columns
head_columns_in_order = ['TicketID', 'TicketType', "Location of Issue",
                         "Asset Ownership ", "PSI Owned Asset Types",
                         "Hardware Type"]

# Filter out the columns from head_columns_in_order
tail_columns = [col for col in joined.columns.tolist()
                if col not in head_columns_in_order]

# Reorder the columns and export it
ordered_table = joined[head_columns_in_order + tail_columns]
ordered_table.to_csv("it_report.csv")
print("Exported the report to it_report.csv")
