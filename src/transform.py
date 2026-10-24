import logging
import re
import pandas as pd
from config import ISO_FORMAT, STATECODE_MAP
from decimal import Decimal, InvalidOperation

logger= logging.getLogger(__name__)

EMAIL_PATTERN= re.compile(r".+@.+\..+")

# Split full name into first and last name
def split_name(full_name):
    if pd.isna(full_name):
        return None, None
    parts= full_name.split()
    first_name= parts[0]
    last_name= " ".join(parts[1:]) or None
    return first_name, last_name


# Lowercase and validate email, invalid ones become empty
def clean_email(email, contact_id):
    if pd.isna(email):
        return None
    email= email.strip().lower()

    if not EMAIL_PATTERN.match(email):
        logger.warning("Invalid email for contact_id %s: %s", contact_id, email)
        return None
    return email

# Convert any date format to ISO 8601 (UTC)
def convert_to_iso(value, record_id):
    if pd.isna(value):
        logger.warning("Missing date for record_id %s", record_id)
        return None
    parsed_date= pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(parsed_date):
        logger.warning("Invalid date for record_id %s: %s", record_id, value)
        return None
    return parsed_date.strftime(ISO_FORMAT)

# Map status text to CDM statecode
def map_status(status, record_id):
    if pd.isna(status):
        return None
    statecode= STATECODE_MAP.get(status.strip().lower())
    if statecode is None:
        logger.warning("Unknown status for record_id %s: %s", record_id, status)
    return statecode

# Parse amount as exact decimal, invalid ones become empty
def parse_amount(amount, record_id):
    if pd.isna(amount):
        logger.warning("Missing amount for record_id %s", record_id)
        return None
    try:
        return Decimal(amount.strip())
    except InvalidOperation:
        logger.warning("Invalid amount for record_id %s: %s", record_id, amount)
        return None


# Build the CDM Contact entity from raw customers
def transform_customers(customers_df):
    contacts=[]
    for _, row in customers_df.iterrows():
        contact_id= row["cust_id"].strip()
        first_names, last_names= split_name(row["full_name"])
        contacts.append({
            "contactid": contact_id,
            "firstname": first_names,
            "lastname": last_names,
            "emailaddress1": clean_email(row["email_addr"], contact_id),
            "createdon": convert_to_iso(row["signup_date"], contact_id),
            "statecode": map_status(row["user_status"], contact_id),

        })
    contacts_df= pd.DataFrame(contacts)
    contacts_df["statecode"]= contacts_df["statecode"].astype("Int64")
    logger.info("Transformed %d customers into contacts", len(contacts_df))
    return contacts_df

# Build the CDM SalesOrder entity, orphan orders are logged and skipped
def transform_orders(orders_df,  contacts_df):
    valid_contact_ids= set(contacts_df["contactid"])
    orders=[]
    for _,row in orders_df.iterrows():
        order_id= row["tx_id"].strip()
        customer_id= row["customer_id"].strip()
        if customer_id not in valid_contact_ids:
            logger.warning("Orphan order %s for unknown customer_id %s", order_id, customer_id)
            continue
        orders.append({
            "salesorderid": order_id,
            "customerid": customer_id,
            "totalamount": parse_amount(row["amount_usd"], order_id),
            "createdon": convert_to_iso(row["tx_timestamp"], order_id),
        })
    orders_df_clean= pd.DataFrame(orders)
    logger.info("Transformed %d orders into sales orders", len(orders_df_clean))
    return orders_df_clean