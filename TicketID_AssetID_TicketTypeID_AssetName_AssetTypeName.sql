/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) htblticket.ticketid as TicketID
      ,htblticket.assetid as AssetID
      ,htblticket.tickettypeid as TicketTypeID
	  ,tblassets.AssetName as AssetName
	  ,tsysAssetTypes.AssetTypename as AssetTypeName
  FROM [lansweeperdb].[dbo].[htblticket]
	INNER JOIN tblassets
		ON htblticket.assetid = tblassets.assetid
	INNER JOIN tsysAssetTypes
		ON tblassets.AssetType = tsysAssetTypes.AssetType
  WHERE h[dbo].[htblcalendarsettings]tblticket.ticketid = 100;