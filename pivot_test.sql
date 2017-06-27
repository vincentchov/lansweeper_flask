/* Reset the temporary pivot table */

if not exists (SELECT * FROM sys.tables where name='PrePivotTempTable')
	CREATE table PrePivotTempTable
		([TicketID]  int,
		 [FieldID]   int,
		 [FieldName] nvarchar(max),
		 [FieldData] nvarchar(max)
	)
go

DELETE FROM PrePivotTempTable

/* Populate the PrePivotTempTable with the FieldName and FieldData to be pivotted */

INSERT INTO 
    PrePivotTempTable ([TicketID],[FieldID],[FieldName],[FieldData])
SELECT TOP (1000) htblticketcustomfield.ticketid as [TicketID]
	  , htblticketcustomfield.fieldid as [FieldID]
	  , htblcustomfields.name as [FieldName]
	  , htblticketcustomfield.data as [FieldData]
  FROM [lansweeperdb].[dbo].[htblticketcustomfield]
	INNER JOIN htblcustomfields
		ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
  WHERE [lansweeperdb].[dbo].[htblticketcustomfield].fieldid NOT IN (27,41,42,43,45,52,88)
  ORDER BY [TicketID],[FieldID];

/* Build the dynamic query that performs the pivotting */

DECLARE @cols AS NVARCHAR(MAX),
    @query  AS NVARCHAR(MAX)

select @cols = STUFF((SELECT DISTINCT ',' + QUOTENAME(FieldName)
                    from (select DISTINCT  
				 TicketID
				, FieldData
				, FieldName
                from PrePivotTempTable
				) x
				group by  FieldName, TicketID
            FOR XML PATH(''), TYPE
            ).value('.', 'NVARCHAR(MAX)')
		,1,1,'')

set @query = 'SELECT DISTINCT TicketID AS TicketID, ' + @cols + ' from 
             (
                select TicketID
				, FieldData
				, FieldName
                from PrePivotTempTable
            ) x
            pivot 
            (
                max(FieldData)
                for FieldName in (' + @cols + ')
            ) p '

EXEC(@query);