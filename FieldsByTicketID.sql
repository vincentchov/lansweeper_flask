/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [TicketID] as [TicketID]
      ,[FieldID] as [FieldID]
      ,[FieldName] as [FieldName]
      ,[FieldData] as [FieldData]
  FROM [lansweeperdb].[lansweeperuser].[TempTable];