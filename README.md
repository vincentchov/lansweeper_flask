# Lansweeper Ticket Report
Making the Lansweeper's ticket info easier to read.

This project uses Kenneth Reitz's [Records](https://github.com/kennethreitz/records)
library in addition to PyODBC to connect to the lansweeperdb MS-SQL Server database.  
Records makes it easier to export results of SQL queries and make it easier to
explore the database to learn its schema.  

## Setup
1. Install [Python 3.x](https://www.python.org/downloads/) and
[Microsoft ODBC Driver 11 for SQL Server](https://www.microsoft.com/en-us/download/details.aspx?id=36434)
2. Create a DSN (Data Source Name) that connects to the ```PSI-SQL``` server,
defaulting to the ```lansweeperdb``` database and use SQL authentication.
3. Update the ```server``` variable to match the name of the DSN
4. Create a secrets.py file with the two strings ```sql_user``` and ```sql_passwd```
5. Create and activate a virtual environment
6. Install dependencies: ```pip install records pyodbc```
7. Profit!

## How to get a Report
All you have to do is choose what kind of report you'd like, whether it's for IT
 Support tickets, etc, and then run the corresponding Python module.  For example,
 if you want to see a table for IT Support tickets, activate your virtual
 environment and then run ```python it_report.py``` at which point it will put the
 resulting table in a .xlsx file
