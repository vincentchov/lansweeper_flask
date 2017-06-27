/****** Script for SelectTopNRows command from SSMS  ******/

if not exists (SELECT * FROM sys.tables where name='TempTable')
	CREATE table TempTable
		([TicketID]  int,
		 [FieldID]   int,
		 [FieldName] nvarchar(max),
		 [FieldData] nvarchar(max)
	)
go

DELETE FROM TempTable

INSERT INTO 
    TempTable ([TicketID],[FieldID],[FieldName],[FieldData])
SELECT TOP (1000) htblticketcustomfield.ticketid as [TicketID]
	  , htblticketcustomfield.fieldid as [FieldID]
	  , htblcustomfields.name as [FieldName]
	  , htblticketcustomfield.data as [FieldData]
  FROM [lansweeperdb].[dbo].[htblticketcustomfield]
	INNER JOIN htblcustomfields
		ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
  WHERE [lansweeperdb].[dbo].[htblticketcustomfield].fieldid NOT IN (27,41,42,43,45,52)
  ORDER BY [TicketID],[FieldID];