import os

PSI_DB_HOST = 'PSI-SQL-DSN'

AWS_HOST = 'AWS-DSN'
AWS_NAME = 'lansweeperdb'
AWS_USER = 'vincenzo'
AWS_PASS = 'mysecretpassword'

def get_sql_uri():
    if os.name == 'posix':
        MS_SQL_URI = "mssql://{}:{}@{}".format(AWS_USER,
                                               AWS_PASS,
                                               AWS_HOST)
    else:
        MS_SQL_URI = "mssql://{}".format(PSI_DB_HOST)

    return MS_SQL_URI
