/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) htblticketcustomfield.ticketid as TicketID
      ,htblcustomfields.fieldid as FieldID
	  ,htblcustomfields.name as FieldName
	  ,htblticketcustomfield.data as FieldData
  FROM [lansweeperdb].[dbo].[htblticketcustomfield]
	INNER JOIN htblcustomfields
		ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
  WHERE htblticketcustomfield.ticketid = 100;