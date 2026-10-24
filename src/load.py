import logging
from config import CONTACT_FILE, SALES_ORDER_FILE

logger= logging.getLogger(__name__)

# Write a table to CSV, create the folder if missing
def write_csv(df, path):
    path.parent.mkdir(parents=True, exist_ok= True)
    df.to_csv(path, index= False)
    logger.info("Wrote %d rows to %s", len(df), path.name)

# Write the CDM entities into the lakehouse
def load(contacts_df, sales_orders_df):
    write_csv(contacts_df, CONTACT_FILE)
    write_csv(sales_orders_df, SALES_ORDER_FILE)
