import os
import json
import gspread

from random import randint
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    def __init__(self, filename):
        print("sheet being made")
        self.filename = filename
        # use creds to create a client to interact with the Google Drive API
        #scope = ['https://spreadsheets.google.com/feeds']
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        keyfile = {}
        keyfile["type"] = os.environ.get("type")
        keyfile["project_id"] = os.environ.get("project_id")
        keyfile["private_key_id"] = os.environ.get('private_key_id')
        keyfile["private_key"] = os.environ.get('private_key').replace("\\n", "\n")
        keyfile["client_email"] = os.environ.get('client_email')
        keyfile["client_id"] = os.environ.get('client_id')
        keyfile["auth_uri"] = os.environ.get('auth_uri')
        keyfile["token_uri"] = os.environ.get('token_uri')
        keyfile["auth_provider_x509_cert_url"] = os.environ.get('auth_provider_x509_cert_url')
        keyfile["client_x509_cert_url"] = os.environ.get('client_x509_cert_url')

        keyfile2 = json.loads(os.environ.get('gsheet_json'))
        with open('client_secret2.json', 'w+') as f:
            json.dump(keyfile2, f)

        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, './client_secret.json')
        f = open(filepath, "r")
        newkeyfile = json.load(f)

        tempKeyfile = {"type": "service_account", "project_id": "flashcardtelegrambot", "private_key_id": "686ed66f906c957d312079cdfd74f7fbb6f046a7", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDBeucB2PNdyoSP\\nNyJQ9naDFNNVzANsA60fyQXyngZiq2ST/4uH1Ds9fpDPW1uW5VumJ45KAWKW6lI2\\nkAPTqfgOaGJPPxhunZmnAhkNJo0ePX8OTM9opyt8K/3u1+lvoPTgHiowMvB8pnCp\\n3bgSgC48bmkEwgvK4mkxbrWt7DoDhqK+QB06s14ifUbACW7Zah8Hzj46+1yhAqJ1\\nOQpbxOavdHo1GNLPIUCvU7n/IVYCx3FtEnurw82ZhQfivoQZpCGh/NIXBrNCSMa+\\n/9yH2TYZowh5bCcvECdNht8A9Xr2ovihwibM57duNiMbl3llTJdWwMqqxQPFDDVO\\nS3bXLP1LAgMBAAECggEAAfDeUWGGzZh+uTKI01wYP4XIIEf5vs/yOo3D/mijWSkL\\nddEDjGobczo9gXI1EdY2caawzH0N727ll+a6ixlUoatNZjulkan4M8qobeBgSymZ\\nf9vsqev+2oL/qfWtH5PIm79ZL3ZC0nds1bS7QdFSOsA7D2aXmGzuja5cVROeV+Zc\\nW2Iw4J2/AIp9kJEjogk6PquQQujS4shvp1kuCXlmiVFqiSPDy4uIQMwTz3sZSyDb\\npdzu2yTInA+PdoAZi5YAAy/Fw0GL2rGYLmrdSteGVxvWQ0kPoqFsZiM4H/4WFUvo\\nakiJmgv7OLmHQTueXg1FHmzlMw/JBDom7OU4J0eI+QKBgQDmInIZfdF66YgYubLg\\nnWgl3/FOEx3HVOkK5KC1J/I/p+zuHY/oct4hruK3f9CMMfXBFMVMy1xzV28L5dTt\\npybPQhfwfMBkiK1HzT1u4yrn1B0uZxEERf3H4Z0kaMf07L6+mZz9opL9/yVIgNxY\\nny9eQtqbKKv0z+65VBx2/Xn2mQKBgQDXOdCWOYfq7K2yrn1QMBGYaxuk4jIpQ5bz\\nCg9Fq6nXBXigIww0jIX3tqcN9jTnofR/MgFwURDPBRRkPmWeGQ3kHdvd+FyJsIP8\\neuYebN/KpMb7f7bX51KVy8ZFDtxHmYQiBc0f9LExCkIsCqcjmhx0oXbIlRffbwiN\\nrRrz3ttVgwKBgQCPUNI3l8gVwEs2AqcoBD6wn4aZtYPs967tTrXaOxc8lyoQm65b\\n9vToiw27csiAFjjSVkoMafSYC9Im2alBmr+rgKCB7l6t/QPUXDcu0B+PIeROWncZ\\nbzD9Aj6nRu2HVMvwzJ8cwNrDfNpODZmrQu7vx7h1ud1kZv1mwr+7Rl1muQKBgQDE\\nVghzUk4sP/aAnu7QHNmgSm0wb+xEelUUpyOhceUAswwEQZSbx2lavXQNp4FBoRuS\\ngQKQ/FKyF7cvb0ByBfcHFzoAdtWsAauVwmN0c+t/R+wBd9NLh8ltvzPCwbivVFsW\\nUmZ6dVTDINGWra0lLCwzNSxP9LqPaBHMdJK2z6EUkwKBgQCETPCl47pTtwxz+vDn\\n5G4Q2AwPPLnPb+BaL0TOS2x2/ieCtc0oi/olwyz0Gjzyw4kPeDeaUK2GdiAw9kZ7\\nBxUi8YbUbfqHrJe8uKH9cKESP0V+WLaLhqXtBpL8bnp7d951lrIKyejdv6akYQmR\\nlJ0AHrK2t0P7FkTlJxAE1HvO5w==\\n-----END PRIVATE KEY-----\\n", "client_email": "admin-437@flashcardtelegrambot.iam.gserviceaccount.com", "client_id": "118311397531265320618", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-437%40flashcardtelegrambot.iam.gserviceaccount.com"}

        creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile, scope)
        client = gspread.authorize(creds)
        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open(filename).sheet1
    def __initreal__(self, filename):
        print("sheet being made")
        self.filename = filename
        # use creds to create a client to interact with the Google Drive API
        #scope = ['https://spreadsheets.google.com/feeds']
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, '../secrets/client_secret.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            filepath, scope)
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
