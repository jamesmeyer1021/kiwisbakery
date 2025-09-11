# sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
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
