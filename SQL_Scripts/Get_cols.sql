DECLARE @my_cols AS NVARCHAR(MAX)

WITH cols(col_string)
AS (
	SELECT [lansweeperdb].[dbo].[get_lansweeper_cols]('(15, 106)', 'Export Compliance')
) 
SELECT @my_cols = cols.col_string FROM cols;

SELECT @my_cols