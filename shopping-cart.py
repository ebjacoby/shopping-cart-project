from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

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

# for row in products:
#     print(row) #> <class 'dict'>

# shopping_cart.py

print("Hello")

def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

subtotal_price = 0
selected_ids = []

while True: 
    selected_id = input("Please input a product identifier: ") #> "9" (string) 
    #> DONE
    if selected_id == "DONE":
        break
    else:
        selected_ids.append(selected_id)


print("---------------------------------")
print("LUCKY'S FOODS GROCERY")
print("WWW.LUCKYS-FOODS-GROCERY.COM")
print("---------------------------------")

current_time = datetime.datetime.now()
print("CHECKOUT AT: ", str(current_time))

print("---------------------------------")
print("SELECTED PRODUCTS:")

for selected_id in selected_ids:
    matching_products = [p for p in products if str(p["id"]) == str(selected_id)] #needs to match previous data type
    matching_product = matching_products[0]  # DO I NEED THIS??!
    subtotal_price = subtotal_price + matching_product["price"]
    print("... " + matching_product["name"] + "  (" + str(to_usd(matching_product["price"])) + ")")

print("---------------------------------")

total_tax = TAX * subtotal_price
total_price = subtotal_price + total_tax

print("SUBTOTAL: " + str(to_usd(subtotal_price)))
print("TAX: " + str(to_usd(total_tax)))
print("TOTAL: " + str(to_usd(total_price)))
print("---------------------------------")
print("THANKS, SEE YOU AGAIN SOON!")
print("---------------------------------")


# exception>>>>>>>>>>>>>>>
# while True:
#     try:
#         x = int(input("Please enter a number: "))
#         break
#     except ValueError:
#         print("Oops!  That was no valid number.  Try again...")

# except (RuntimeError, TypeError, NameError):
#     pass
