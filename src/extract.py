import logging
import pandas as pd
from config import RAW_CUSTOMERS, RAW_ORDERS

logger= logging.getLogger(__name__)

# Read CSV as text
def read_csv(path):
    df= pd.read_csv(path, dtype=str)
    logger.info("Read %d rows from %s", len(df), path.name)
    return df

# Read raw sources
def extract():
    customers_df= read_csv(RAW_CUSTOMERS)
    orders_df= read_csv(RAW_ORDERS)
    return customers_df, orders_df