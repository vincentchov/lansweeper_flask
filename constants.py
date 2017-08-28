SQL_FRAGMENTS = {
    "ADMIN_BUS_DEV": {
        "fieldid": "(154,155,156)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Administrative / Business Development",
        "group_by": ""
    },

    "IT_SUPPORT": {
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
                    """
    },

    "CUSTOMER_VENDOR_RELATED": {
        "fieldid": "(124,125,126,127,128)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Customer / Vendor Related",
        "group_by": ""
    },

    "EH_AND_S": {
        "fieldid": "(15,41,123)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "EH & S - Environmental Health & Safety",
        "group_by": ""
    },

    "ENGINEERING": {
        "fieldid": "(15,108,110)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Engineering ",
        "group_by": ""
    },

    "EXPORT_COMPLIANCE": {
        "fieldid": "(15,106)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Export Compliance",
        "group_by": ""
    },

    "FACILITY_MAINTENANCE": {
        "fieldid": "(15,43,41,42,142,45)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Facility / Maintenance",
        "group_by": ""
    },

    "HUMAN_RESOURCES": {
        "fieldid": "(15,130,133,131)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Human Resources",
        "group_by": ""
    },

    "PROJ_MGMT_MGMT_ISSUES": {
        "fieldid": "(15,146,147,148,150)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Project Management / Management Issues",
        "group_by": ""
    },

    "PURCHASING_AND_ACCOUNTING": {
        "fieldid": "(15,109,110)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Purchasing & Accounting",
        "group_by": ""
    },

    "QUALITY": {
        "fieldid": "(151,153,152)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Quality",
        "group_by": ""
    },

    "SECURITY": {
        "fieldid": "(15,50,51,53,52,45,135,137,136,138)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Security ",
        "group_by": ""
    },

    "SHOP_OPERATIONS": {
        "fieldid": "(41,112,116,111,114,115,113,120,117,118,122,121)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Shop Operations",
        "group_by": ""
    },

    "TIMESHEET_SYSTEM": {
        "fieldid": "(129,110)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Timesheet System",
        "group_by": ""
    },

    "TRAINING": {
        "fieldid": "(15,107)",
        "to_join": "",
        "select": "",
        "join": "",
        "typename": "Training",
        "group_by": ""
    }
}
