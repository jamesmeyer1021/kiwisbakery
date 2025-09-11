# sheets.py
import gspread
import os
from google.oauth2 import service_account

creds_dict = {
    "type": os.environ["GOOGLE_TYPE"],
    "project_id": os.environ["GOOGLE_PROJECT_ID"],
    "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
    "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace('\\n', '\n'),
    "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
    "client_id": os.environ["GOOGLE_CLIENT_ID"],
    "auth_uri": os.environ["GOOGLE_AUTH_URI"],
    "token_uri": os.environ["GOOGLE_TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["GOOGLE_AUTH_PROVIDER_CERT_URL"],
    "client_x509_cert_url": os.environ["GOOGLE_CLIENT_CERT_URL"],
    "universe_domain": os.environ["GOOGLE_UNIVERSE_DOMAIN"]
}

def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("KiwisOrders")

def log_order(order_number, customer_name, customer_email, customer_phone, order_date):
    orders_tab = get_sheet().worksheet("Orders")
    try:    
        orders_tab.append_row([order_number, customer_name, customer_email, customer_phone, order_date], value_input_option='USER_ENTERED')
    except Exception as e:
        print("Error writing to sheet:", e)

def log_order_item(order_number, item_name, quantity, price):
    items_tab = get_sheet().worksheet("Order_Items")
    total = quantity * price
    try:
        items_tab.append_row([None, order_number, item_name, quantity, price, total], value_input_option='USER_ENTERED')
    except Exception as e:
        print("Error writing to sheet:", e)
