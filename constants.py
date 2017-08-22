IT_SUPPORT = {
    "fieldid": """
                    (45,43,15,55,56,58,57,88,60,104,105,
                     83,85,100,103,101,102,84,90,89)
               """,
    "to_join": "AssetName, AssetTypeName, ",
    "select": """
                    tblassets.AssetName as AssetName,
                    tsysAssetTypes.AssetTypename as AssetTypeName,\n
              """,
    "join": """
                INNER JOIN tblassets
                    ON htblticket.assetid = tblassets.assetid
                INNER JOIN tsysAssetTypes
                    ON tblassets.AssetType = tsysAssetTypes.AssetType\n
            """,
    "typename": "IT Support",
    "group_by": """
                    tblassets.AssetName,
                    tsysAssetTypes.AssetTypename,\n
                """,

}
