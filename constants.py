ADMIN_BUS_DEV = {
    "fieldid": "(154,155,156)",
    "typename": "Administrative / Business Development"
}

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
                """
}

CUSTOMER_VENDOR_RELATED = {
    "fieldid": "(124,125,126,127,128)",
    "typename": "Customer / Vendor Related"
}

EH_AND_S = {
    "fieldid": "(15,41,123)",
    "typename": "EH & S - Environmental Health & Safety"
}

ENGINEERING = {
    "fieldid": "(15,108,110)",
    "typename": "Engineering "
}

EXPORT_COMPLIANCE = {
    "fieldid": "(15,106)",
    "typename": "Export Compliance"
}

FACILITY_MAINTENANCE = {
    "fieldid": "(15,43,41,42,142,45)",
    "typename": "Facility / Maintenance"
}

HUMAN_RESOURCES = {
    "fieldid": "(15,130,133,131)",
    "typename": "Human Resources"
}

PROJ_MGMT_MGMT_ISSUES = {
    "fieldid": "(15,146,147,148,150)",
    "typename": "Project Management / Management Issues"
}

PURCHASING_AND_ACCOUNTING = {
    "fieldid": "(15,109,110)",
    "typename": "Purchasing & Accounting"
}

QUALITY = {
    "fieldid": "(151,153,152)",
    "typename": "Quality"
}

SECURITY = {
    "fieldid": "(15,50,51,53,52,45,135,137,136,138)",
    "typename": "Security "
}

SHOP_OPERATIONS = {
    "fieldid": "(41,112,116,111,114,115,113,120,117,118,122,121)",
    "typename": "Shop Operations"
}

TIMESHEET_SYSTEM = {
    "fieldid": "(129,110)",
    "typename": "Timesheet System"
}

TRAINING = {
    "fieldid": "(15,107)",
    "typename": "Training"
}
