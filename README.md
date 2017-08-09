# Lansweeper Ticket Reports: Making the Lansweeper's ticket info easier to read.

This project uses Kenneth Reitz's [Records](https://github.com/kennethreitz/records)
library in addition to PyODBC to connect to the lansweeperdb MS-SQL Server database.  
Records makes it easier to export results of SQL queries and make it easier to
explore the database to learn its schema.  

## Setup
1. Install [Python 3.x](https://www.python.org/downloads/) with pip and
[Microsoft ODBC Driver 11 for SQL Server](https://www.microsoft.com/en-us/download/details.aspx?id=36434)
which you may already have in Windows, but typically not in other systems.
2. If you're in Windows, open up the Data Sources program.  If you're in Linux,
edit the ~/.odbc.ini file in the next step.
3. Create a DSN (Data Source Name) that connects to the ```PSI-SQL``` server,
defaulting to the ```lansweeperdb``` database and use SQL authentication.
4. Update the ```server``` variable to match the name of the DSN
5. Create a secrets.py file with the two strings ```sql_user``` and ```sql_passwd```
6. Create and activate a virtual environment
7. Install dependencies: ```pip install records pyodbc```
8. Profit!

## How to get a Report
All you have to do is choose what kind of report you'd like, whether it's for IT
 Support tickets, etc, and then run the corresponding Python module.  For example,
 if you want to see a table for IT Support tickets, activate your virtual
 environment and then run ```python it_support.py``` at which point it will put the
 resulting table in a .xls file in the Reports folder called ```it_support.xls```
