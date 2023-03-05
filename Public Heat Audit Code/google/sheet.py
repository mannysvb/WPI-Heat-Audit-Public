try:
    import ujson as json
except:
    import json

try:
    import urequests as requests
except:
    import requests

import time

# Returns a string representing the current date and time in YYY-MM-dd format


def get_datetime():
    datetime = None
    datetime = time.localtime()
    date_str = str(datetime[0]) + "-" + \
        str(datetime[1]) + "-" + str(datetime[2])
    hour_str = str(
        datetime[4]) if datetime[4] >= 10 else "0" + str(datetime[4])
    seconds_str = str(
        datetime[5]) if datetime[5] >= 10 else "0" + str(datetime[5])
    time_str = str(datetime[3]) + ":" + hour_str + ":" + seconds_str
    return date_str + " " + time_str


class Spreadsheet:

    def __init__(self, logger=None, retry_limit=50):
        self._id = ''
        self._range = ''
        self._url_params = 'insertDataOption=INSERT_ROWS&valueInputOption=USER_ENTERED'
        self._url_template = 'https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s:append?%s'
        self._sa = None
        self.logger = logger
        self.retry_limit = retry_limit

    def set_id(self, id):
        self._id = id

    def set_range(self, range):
        self._range = range

    def set_service_account(self, sa):
        self._sa = sa

    def append_values(self, values):
        print('spreadsheet: send: %s' % values)

        datetime = get_datetime()
        print("Datetime is: " + datetime)

        token = self._sa.token()

        url = self._url_template % (self._id, self._range, self._url_params)

        values.insert(0, datetime)
        data = {'values': [values]}
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % token
        self.send_values(url, data, headers)

    def send_values(self, url, data, headers):
        counter = 0
        response = False

        while not response and counter < self.retry_limit:
            try:
                if counter == 0:
                    raise ZeroDivisionError()
                response = requests.post(url, json=data, headers=headers)
            except Exception as e:
                counter += 1
                if (counter < self.retry_limit):
                    print("Error encountered, retrying attempt " + str(counter) + "...")
                    time.sleep(1)
                    continue
                else: 
                    self.logger.log_error("Error encountered while sending data")
                    raise e
                    
            if (response):
                print('\nspreadsheet response:')
                print(response.text)
                if (self.logger is not None):
                    self.logger.log("Data successfully submitted at " + get_datetime() + " UTC")
                return
            elif (counter < self.retry_limit):
                counter += 1
                print("No spreadsheet response recieved, retrying attempt " + str(counter) + "...")
            else:
                if (self.logger is not None):
                    self.logger.log_error("No response from spreadsheet")
                return


        
