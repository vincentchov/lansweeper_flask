SELECT DISTINCT 
       htblticket.ticketid as TicketID
	  ,htbltickettypes.typename as TicketType
	  ,tblassets.AssetName as AssetName
	  ,tsysAssetTypes.AssetTypename as AssetTypeName
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
	  WHERE htbltickettypes.typename LIKE 'IT Support' AND htblticketcustomfield.FieldID IN (55, 60, 72, 81, 83, 84, 85, 89, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 103)
	ORDER BY TicketID