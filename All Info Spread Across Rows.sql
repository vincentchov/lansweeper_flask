/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) htblticket.ticketid as TicketID
	  ,htbltickettypes.typename as TicketType
      ,htblticket.assetid as AssetID
      ,htblticket.tickettypeid as TicketTypeID
	  ,tblassets.AssetName as AssetName
	  ,tsysAssetTypes.AssetTypename as AssetTypeName
	  ,htblcustomfields.fieldid as FieldID
	  ,htblcustomfields.name as FieldName
	  ,htblticketcustomfield.data as FieldData
  FROM [lansweeperdb].[dbo].[htblticket]
  	/* FieldData */
	INNER JOIN htblticketcustomfield 
		ON htblticket.ticketid = htblticketcustomfield.ticketid
	/* FieldName */
	INNER JOIN htblcustomfields
		ON htblticketcustomfield.fieldid = htblcustomfields.fieldid
	/* AssetName */
	INNER JOIN tblassets
		ON htblticket.assetid = tblassets.assetid
	/* AssetTypeName */
	INNER JOIN tsysAssetTypes
		ON tblassets.AssetType = tsysAssetTypes.AssetType

	/* TicketType */
	INNER JOIN htbltickettypes
		ON htblticket.tickettypeid = htbltickettypes.tickettypeid
  WHERE htbltickettypes.typename LIKE 'IT Support';
