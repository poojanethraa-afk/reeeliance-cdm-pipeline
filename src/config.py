from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

#Input
RAW_DIR= BASE_DIR / "data" / "raw"
RAW_CUSTOMERS = RAW_DIR / "raw_customers.csv"
RAW_ORDERS = RAW_DIR / "raw_orders.csv"

# Output (CDM lakehouse)
LAKEHOUSE_DIR = BASE_DIR / "cdm_lakehouse"
CONTACT_FILE = LAKEHOUSE_DIR / "Contact" / "Contact.csv"
SALES_ORDER_FILE = LAKEHOUSE_DIR / "SalesOrder" / "SalesOrder.csv"
MANIFEST_FILE = LAKEHOUSE_DIR / "model.json"

# Logging
LOG_DIR= BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

# Business rules
STATECODE_MAP= { "active": 0, "inactive": 1}
ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"