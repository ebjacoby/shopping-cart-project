from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "products")

TAX = os.environ.get("TAX", "OOPS, please set env var called 'TAX'")
TAX = float(TAX)

print(DOCUMENT_ID)

#
# AUTHORIZATION
#

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

#
# READ SHEET VALUES
#

client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>

doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>

print("-----------------")
print("SPREADSHEET:", doc.title)
print("-----------------")

sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

products = sheet.get_all_records() #> <class 'list'>

#
# WRITE VALUES TO SHEET for GOOGLE SHEET API 
#

#next_id = len(products) + 1 # TODO: should change this to be one greater than the current maximum id value
next_id = max(p["id"] for p in products) + 1
product_name = input("Please enter the name of the new product: ")
aisle_name = input("Please enter the name of the aisle in which " + product_name + " will be placed: ")
department_name = input("Please enter the name of the department for " + product_name + ": ")
product_price = float(input("Please enter the price of " + product_name + ": "))

next_object = {
    "id": next_id,
    "name": product_name,
    "aisle": aisle_name.lower(),
    "department": department_name.lower(),
    "price": product_price
}

next_row = list(next_object.values()) #> [13, 'Product 13', 'snacks', 4.99, '2019-01-01']

next_row_number = len(products) + 2 # number of records, plus a header row, plus one

response = sheet.insert_row(next_row, next_row_number)

print("-----------------")
print("NEW RECORD:")
print(next_row)
print("-----------------")
