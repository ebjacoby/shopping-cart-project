from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

id_list = [p["id"] for p in products]
max_id = max(id_list)

# for row in products:
#     print(row) #> <class 'dict'>

# shopping_cart.py

print("Hello")

def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

subtotal_price = 0
selected_ids = []

while True: 
    selected_id = input("Please input a unique product identifier (up to " + str(max_id) + ") or enter 'DONE' when finished: ") #> "9" (string) 
    #> DONE
    if selected_id.lower() == "done":
        break
    elif not selected_id.isnumeric():
        continue
    elif int(selected_id) not in id_list:
        continue
    else:
        selected_ids.append(selected_id)      

print("---------------------------------")
print("LUCKY'S FOODS GROCERY")
print("WWW.LUCKYS-FOODS-GROCERY.COM")
print("---------------------------------")

current_day = datetime.date.today()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
full_time = str(current_day) + " " + str(current_time)

print("CHECKOUT AT: ", full_time)

print("---------------------------------")
print("SELECTED PRODUCTS:")

for selected_id in selected_ids:
    matching_products = [p for p in products if str(p["id"]) == str(selected_id)] #needs to match previous data type
    matching_product = matching_products[0]  # DO I NEED THIS??!
    subtotal_price = subtotal_price + matching_product["price"]
    print("... " + matching_product["name"] + "  (" + str(to_usd(matching_product["price"])) + ")")

all_matching_products = [p for p in products if str(p["id"]) in str(selected_ids)] #new list - dictionaries of selected products

print("---------------------------------")

total_tax = TAX * subtotal_price
total_price = subtotal_price + total_tax

print("SUBTOTAL: " + str(to_usd(subtotal_price)))
print("TAX: " + str(to_usd(total_tax)))
print("TOTAL: " + str(to_usd(total_price)))
print("---------------------------------")
print("THANKS, SEE YOU AGAIN SOON!")
print("---------------------------------")


#Send e-mail receipt
customer_email = input("Please enter your e-mail for an electronic copy of your receipt: ")

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

#print("API KEY:", SENDGRID_API_KEY)
#print("TEMPLATE ID:", SENDGRID_TEMPLATE_ID)
#print("EMAIL ADDRESS:", MY_ADDRESS)

template_data = {
    "total_price_usd": str(to_usd(total_price)),
    "human_friendly_timestamp": full_time,
    "products": all_matching_products
} # or construct this dictionary dynamically based on the results of some other process :-D

client = SendGridAPIClient(SENDGRID_API_KEY)
print("CLIENT:", type(client))

message = Mail(from_email=MY_ADDRESS, to_emails=customer_email)
print("MESSAGE:", type(message))

message.template_id = SENDGRID_TEMPLATE_ID

message.dynamic_template_data = template_data

try:
    response = client.send(message)
    print("RESPONSE:", type(response))
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as e:
    print("OOPS", e)