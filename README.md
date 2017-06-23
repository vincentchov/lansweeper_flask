# Lansweeper Ticket Report
Making the Lansweeper's ticket info easier to read.

This project uses Kenneth Reitz's [Records](https://github.com/kennethreitz/records) library in addition to the PyODBC driver to connect to the lansweeperdb MS-SQL Server database.  Records makes it easier to export results of SQL queries and make it easier to explore the database to learn its schema.  

## Setup
1. Install Python 3.4 and Microsft ODBC Driver for SQL Server 11 
2. Create a DSN (Data Source Name) that connects to the ```PSI-SQL``` server, defaulting to the ```lansweeperdb``` database and use SQL authentication.
3. Update the ```server``` variable to match the name of the DSN
4. Create a secrets.py file with the two strings ```sql_user``` and ```sql_passwd```
5. Create and activate a virtual environment
6. Install dependencies: ```pip install records pyodbc```
7. Profit!
