import logging

from config import LOG_DIR, LOG_FILE
from extract import extract
from load import load
from manifest import write_manifest
from transform import transform_customers, transform_orders

# Log to the terminal and to logs/pipeline.log
def setup_logging():
    LOG_DIR.mkdir(parents= True, exist_ok= True)
    logging.basicConfig(
        level= logging.INFO,
        format= "%(asctime)s | %(levelname)-7s | %(name)-9s | %(message)s",
        handlers= [
            logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ],
    )

# Run the full pipeline: extract, transform, load, manifest
def main():
    setup_logging()
    logger= logging.getLogger("pipeline")
    logger.info("Pipeline started")
    customers_df, orders_df = extract()
    contacts_df = transform_customers(customers_df)
    sales_orders_df = transform_orders(orders_df, contacts_df)
    load(contacts_df, sales_orders_df)
    write_manifest()
    logger.info("Pipeline finished")

if __name__ == "__main__":
    main()