# shopping-cart.py

## Setup

### Repo Setup

Navigate to https://github.com/ebjacoby/shopping-cart-project and clone the repository to your desktop.


After cloning the repo (make sure to save it in a directory similar to that shown below), navigate there from the command-line:

```sh
cd ~/Desktop/Github/shopping-cart-project
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n groceries-env python=3.7 # (first time only)
conda activate groceries-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file, included in the cloned repository:

```sh
pip install -r requirements.txt
```

### API SETUP

Visit the [Google Developer Console](https://console.developers.google.com/cloud-resource-manager). Create a new project, or select an existing one. Click on your project, then from the project page, search for the "Google Sheets API" and enable it. Also search for the "Google Drive API" and enable it.

From either API page, or from the [API Credentials](https://console.developers.google.com/apis/credentials) page, follow a process to create and download credentials to use the APIs. Fill in the form to find out what kind of credentials:

  + API: "Google Sheets API"
  + Calling From: "Web Server"
  + Accessing: "Application Data"
  + Using Engines: "No"

The suggested credentials will be for a service account. Follow the prompt to create a new service account with a role of: "Project" > "Editor", and create credentials for that service account. Download the resulting .json file and store it in your project repo in a location like "auth/google_api_credentials.json".

Before committing, add the credentials filepath to your ".gitignore" file to ensure it does not get tracked in version control or uploaded to GitHub. Do the same for all unique identifiers, API Keys, etc.

Save the .json file in the root directory as:

```sh
spreadsheet_credentials.json #and within it the relevant information provided by GOOGLE
```
Note this .json file in the .gitignore as well

The unique identifier of the shared google sheet will also have to be input as an environment variable `GOOGLE_SHEET_ID`. The user can use their own input (or the one provided in class, which for security reasons will not be shared here).



Next, we'll acquire two API Keys from SENDGRID:

First, [sign up for a free account](https://signup.sendgrid.com/), then click the link in a confirmation email to verify your account. Then [create an API Key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions. To setup: store the API Key value in an environment variable called `SENDGRID_API_KEY`. Also set an environment variable called `MY_EMAIL_ADDRESS` to be the email address you just associated with your SendGrid account (e.g. "abc123@gmail.com").

Navigate to https://sendgrid.com/dynamic_templates and press the "Create Template" button on the top right. Give it a name like "example-receipt", and click "Save". At this time, you should see your template's unique identifier (e.g. "d-b902ae61c68f40dbbd1103187a9736f0"). Copy this value and store it in an environment variable called 
`SENDGRID_TEMPLATE_ID`.

Lastly, name an environment variable `TAX` and input, in it, your local state tax rate. 

## Usage

```sh
set MY_EMAIL_ADDRESS=mn001@stern.nyu.edu  #on the right of the equals sign, here, is a fake/placeholder e-mail/key. 
```

You could also load this into a .env file and have it called by writing 'from dotenv import load_dotenv' in your code and then 'load_dotenv()'. If this method does not work, please input environment variables individually, as stated before^.

### run the app

To run the app, type the following into the command line:

```sh
python shopping_cart.py
```

The app will request an inputs: unique identifies for each product, with specific requirements for input. Following input, the app will run and and print, on the command line, an itemized receipt, as well as the subtotal, tax info and total cost. The app will also e-mail a copy of the receipt to a designated recipient, which is input in the command line as well. 

To run the secondary app, type the following into the command line:

```sh
python add_new_product.py
```

This code will allow the user to input new products to the shared google sheet. This app requires the same API Keys as the shopping_cart.py