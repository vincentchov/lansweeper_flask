import collections
SQL_FRAGMENTS = collections.OrderedDict([
    (
        "ADMIN_BUS_DEV",
        {
            "fieldid": "(52,154,155,156)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Administrative / Business Development",
            "group_by": ""
         }
    ),

    (
        "CUSTOMER_VENDOR_RELATED",
        {
            "fieldid": "(52,124,175)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Customer / Vendor Related",
            "group_by": ""
        }
    ),

    (
        "EH_AND_S",
        {
            "fieldid": "(15,41,52,123)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "EH & S - Environmental Health & Safety",
            "group_by": ""
        }
    ),

    (
        "ENGINEERING",
        {
            "fieldid": "(15,52,108,110)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Engineering ",
            "group_by": ""
        }
    ),

    (
        "EXPORT_COMPLIANCE",
        {
            "fieldid": "(15,52,106)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Export Compliance",
            "group_by": ""
        }
    ),

    (
        "FACILITY_MAINTENANCE",
        {
            "fieldid": """
                            (15,41,42,43,45,48,62,63,64,65,66,
                             67,68,69,72,73,74,75,76,78,80,142)
                       """,
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Facility / Maintenance Issues",
            "group_by": ""
        }
    ),

    (
        "HUMAN_RESOURCES",
        {
            "fieldid": "(15,130,131,133,186)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Human Resources",
            "group_by": ""
        }
    ),

    (
        "IT_SUPPORT",
        {
            "fieldid": """
                            (15,43,45,52,55,56,57,58,60,82,83,84,85,
                             88,89,90,91,92,93,94,95,96,97,98,99,100,
                             101,102,103,104,105,157,158,159,160,168,
                             175,177,178,179,180,181,182,183,184)
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
        }
    ),

    (
        "PROJ_MGMT_MGMT_ISSUES",
        {
            "fieldid": "(52,146,147,148,150,173,174,175)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Project Management / Management Issues",
            "group_by": ""
        }
    ),

    (
        "PURCHASING_AND_FINANCE",
        {
            "fieldid": "(15,45,109,126,170,172)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Purchasing & Finance",
            "group_by": ""
        }
    ),

    (
        "QUALITY",
        {
            "fieldid": "(52,151,152,153)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Quality",
            "group_by": ""
        }
    ),

    (
        "SECURITY",
        {
            "fieldid": "(15,45,50,51,52,53,135,136,137,138)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Security ",
            "group_by": ""
        }
    ),

    (
        "SERVICE_MAINTENANCE",
        {
            "fieldid": "(15,187)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Service / Maintenance Request (Non-IT)",
            "group_by": ""
        }
    ),

    (
        "SHOP_OPERATIONS",
        {
            "fieldid": "(41,52,112,161,162,164,166)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Shop Operations",
            "group_by": ""
        }
    ),

    (
        "TIMESHEET_SYSTEM",
        {
            "fieldid": "(129,176)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Timesheet System",
            "group_by": ""
        }
    ),

    (
        "TRAINING",
        {
            "fieldid": "(15,52,107)",
            "to_join": "",
            "select": "",
            "join": "",
            "typename": "Training",
            "group_by": ""
        }
    )
])
