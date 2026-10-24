import json
import logging
from config import CONTACT_FILE, LAKEHOUSE_DIR, MANIFEST_FILE, SALES_ORDER_FILE

logger= logging.getLogger(__name__)

# Attribute definitions per CDM entity
CONTACT_ATTRIBUTES= [
    {"name": "contactid", "dataType": "string", "description": "Unique primary key for the contact"},
    {"name": "firstname", "dataType": "string", "description": "First name of the contact"},
    {"name": "lastname", "dataType": "string", "description": "Last name of the contact"},
    {"name": "emailaddress1", "dataType": "string", "description": "Primary email address"},
    {"name": "createdon", "dataType": "dateTime", "description":"ISO 8601 creation timestamp"},
    {"name": "statecode", "dataType": "int64", "description": "Status code: 0 for Active, 1 for Inactive"},
    ]

SALES_ORDER_ATTRIBUTES= [
    {"name": "salesorderid", "dataType": "string", "description": "Unique order identifier"},
    {"name": "customerid", "dataType": "string", "description": "Foreign key reference to contact"},
    {"name": "totalamount", "dataType": "decimal", "description": "Total order amount in USD"},
    {"name": "createdon", "dataType":"dateTime", "description": "ISO 8601 transaction timestamp"},
]

# Describe one CDM entity with its attributes and CSV partition
def build_entity(name, description, attributes, file_path):
    return{
        "$type": "LocalEntity",
        "name": name,
        "description": description,
        "attributes": attributes,
        "partitions":[
            {
                "name":f"{name}Partitions",
                "location": file_path.relative_to(LAKEHOUSE_DIR).as_posix(),
                "fileFormatSettings":{
                "$type":"CsvFormatSettings",
                "columnHeaders": True,
                "delimiter":",",
                },
            }
        ]

    }

# Build the full CDM manifest
def build_manifest():
    return{
        "name": "EnterpriseDataLake",
        "description": "CDM Manifest for Ingested Customer and Sales Data",
        "version": "1.0",
        "entities": [
            build_entity("Contact", "Standard CDM Contact entity for individual customers", CONTACT_ATTRIBUTES,
                CONTACT_FILE,),
            build_entity( "SalesOrder",
                "Standard CDM SalesOrder entity for transactions",
                SALES_ORDER_ATTRIBUTES,
                SALES_ORDER_FILE,),

        ],
        "relationships": [
            {
                "$type": "SingleKeyRelationship",
                "name": "Contact_SalesOrder_Relationship",
                "fromAttribute": {"entityName": "SalesOrder", "attributeName": "customerid"},
                "toAttribute": {"entityName": "Contact", "attributeName": "contactid"},
            }
        ],
    }

# Write model.json into the lakehouse
def write_manifest():
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(build_manifest(), f, indent=2)
    logger.info("Wrote manifest to %s", MANIFEST_FILE.name)