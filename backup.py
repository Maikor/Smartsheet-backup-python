import json
import os
import requests
import time

token = " Bearer TOKEN_NUMBER"

sheet_id_1 = 123123123L
backed_up_sheets = {"sheet_name_1": sheet_id_1}

dir = 'backup/' + time.strftime("-%m_%d_%Y_%H_%M")


API_URL = "https://api.smartsheet.com/2.0/sheets/"

payload = {"Authorization": token,
           "Accept": "application/vnd.ms-excel"}
payload_attach = {"Authorization": token}

amount = len(backed_up_sheets)


i = 1
for el in backed_up_sheets:
    r = requests.get(API_URL + str(backed_up_sheets[el]), headers=payload)
    if r.status_code != 200:
        print 'Some problem with connections, please retry later'
        pass
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dir + el + time.strftime("-%m_%d_%Y_%H_%M") + ".xls", 'wb') as output:
        output.write(r.content)
    print 'Progress in sheets: ' + str(i) + '/' + str(amount)
    i += 1

for el in backed_up_sheets:
    r = requests.get(API_URL + str(backed_up_sheets[el]) + '/attachments', headers=payload_attach)
    if r.status_code != 200:
        print 'Some problem with connections, please retry later'
        pass
    k = json.loads(r.content)
    j = 1
    amount = len(k['data'])
    if not os.path.exists(dir + el + '/') and k['data'] != []:
        os.makedirs(dir + el + '/')
    for element in k['data']:

        r_get_single_attachment = requests.get(API_URL + str(backed_up_sheets[el]) +
                                               '/attachments/' + str(element['id']),
                                               headers=payload_attach)
        if r_get_single_attachment.status_code != 200:
            print 'Some problem with connections, please retry later'
            pass
        f = json.loads(r_get_single_attachment.content)
        r_download = requests.get(f['url'])
        print 'Grabbing attachments: ' + str(j) + '/' + str(amount) + \
              ' Download {!s}, from {!s}'.format(f['name'], el)
        if r_download.status_code != 200:
            print 'Some problem with connections, please retry later'
            pass
        with open(dir + el + '/' + f['name'], 'wb') as output:
            output.write(r_download.content)
        j += 1
