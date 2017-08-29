# Lansweeper Ticket Reports
This project uses Kenneth Reitz's [Records](https://github.com/kennethreitz/records)
library in addition to PyODBC to connect to the lansweeperdb MS-SQL Server database.  
Records makes it easier to export results of SQL queries and make it easier to
explore the database to learn its schema.  

## Setup from source code
1. Install [Python 3.x](https://www.python.org/downloads/) with pip.
2. Install [Microsoft ODBC Driver 11 for SQL Server](https://www.microsoft.com/en-us/download/details.aspx?id=36434)
which you may already have in Windows, but typically not in other systems.
2. If you're in Windows, open up the Data Sources program.  If you're in Linux,
edit the ~/.odbc.ini file in the next step.
3. Create a DSN (Data Source Name) called ```PSI-SQL-DSN``` that connects to the ```PSI-SQL```
server, defaulting to the ```lansweeperdb``` database and use SQL authentication.
4. Update the ```server``` variable to match the name of the DSN if you chose
something other than ```PSI-SQL-DSN```.
6. Create and activate a virtual environment
7. Install dependencies: ```pip install -r requirements.txt```
8. Profit!

<!--  
## Setup using executables
1. See step 2 from above.
2. See step 3 from above.
-->

## How to get a Report (source code)
All you have to do is run ```lansweeper_all.py``` and enter the number for the
report type you want when asked for it.  For example, if you want to see a
table for Administrative / Business Development tickets, activate your virtual
environment and then run ```python lansweeper_all.py``` at which point it will
list out the different options.  Enter 0 and hit enter.  The resulting table
will be placedin a .xlsx file in the Reports folder called ```admin_bus_dev.xlsx```.

<!--  
## How to get a Report (source code)
All you have to do is run the executable file in your Command Prompt/Terminal
and enter the number for the report type you want when asked for it.  
For example, if you want to see a table for Administrative / Business Development
tickets, drag and drop the executable at which point it will list out the
different options.  Enter 0 and hit enter.  The resulting table will be placed
in a .xlsx file in the Reports folder called ```admin_bus_dev.xlsx```.
-->
