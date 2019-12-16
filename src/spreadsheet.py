import os
import json
import gspread

from random import randint
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    def __initfake__(self, filename):
        print("sheet being made")
        self.filename = filename
        # use creds to create a client to interact with the Google Drive API
        #scope = ['https://spreadsheets.google.com/feeds']
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        # keyfile = {}
        # keyfile["type"] = os.environ.get("type")
        # keyfile["project_id"] = os.environ.get("project_id")
        # keyfile["private_key_id"] = os.environ.get('private_key_id')
        # keyfile["private_key"] = os.environ.get('private_key')
        # keyfile["client_email"] = os.environ.get('client_email')
        # keyfile["client_id"] = os.environ.get('client_id')
        # keyfile["auth_uri"] = os.environ.get('auth_uri')
        # keyfile["token_uri"] = os.environ.get('token_uri')
        # keyfile["auth_provider_x509_cert_url"] = os.environ.get('auth_provider_x509_cert_url')
        # keyfile["client_x509_cert_url"] = os.environ.get('client_x509_cert_url')

        # keyfile = json.loads(os.environ.get('gsheet_json'))
        # with open ('client_secret2.json', "w+") as f:
        #     json.dump(keyfile, f)

        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open(filename).sheet1
    def __init__(self, filename):
        print("sheet being made")
        self.filename = filename
        # use creds to create a client to interact with the Google Drive API
        #scope = ['https://spreadsheets.google.com/feeds']
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            '..\secrets\client_secret.json', scope)
        client = gspread.authorize(creds)
        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open(filename).sheet1

    def get_all_records(self):
        # Extract and print all of the values
        return self.sheet.get_all_records()

    def get_all_values(self):
        # returns a list of list of the values
        return self.sheet.get_all_values()

    def get_question(self):
        data = self.get_all_values()
        dataLength = len(data)  # header
        if dataLength == 0:
            return "No data found"
        else:
            index = randint(0, dataLength - 1)

            print("getting question at index " + str(index))
            question, answer = data[index]
            return (question, answer)

    def setSource(self, filename):
        return Sheet(filename)

with open ('.\\client_secret.json', "r") as f:
    print("IN MAIN")