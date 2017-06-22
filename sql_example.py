import pyodbc
from secrets import sql_user, sql_passwd

# Log into the MS-SQL Server
server = 'PSI-SQL' 
database = 'lansweeperdb' 
username = sql_user
password = sql_passwd
cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Get the custom field info for your ticket number
cursor.execute("SELECT * FROM htblticketcustomfield WHERE htblticketcustomfield.ticketid = 98;") 
row = cursor.fetchone()
# Print out the column names
field_names = [i[0] for i in cursor.description]
print(field_names)
# Print the rows returned
while row: 
    print(row)
    row = cursor.fetchone()
