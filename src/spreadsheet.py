import gspread
from oauth2client.service_account import ServiceAccountCredentials

class sheet:
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

    pass
