import requests
import time
import sys
import json
import os


def download_url(url = "http://localhost:1990/confluence/download/temp/Confluence-space-export-121346-26.xml.zip", save_path = "./test.zip", chunk_size=128):
    r = requests.get(url, stream=True,auth=('admin','admin'))
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


payload = {'os_username': 'admin', 'os_password': 'admin'}
authentication_tuple = ('admin','admin')

base_url = sys.argv[1]      # http://localhost:1990/confluence/
key_list = sys.argv[2].split(',')       # ds


for key in key_list:
    # create request page
    request_page_url = base_url + "/rest/confapi/1/backup/export/" + key

    print(request_page_url)

    response_request_page = requests.get(request_page_url,auth=authentication_tuple)
    s = str(response_request_page.headers)

    s = s.replace("'",'"')
    js = json.loads(s)

    queue_url = js['Location']
    print(queue_url)
    # queue_url = "http://localhost:1990/confluence/rest/confapi/1/backup/queue/a1282066-cc00-4530-a226-ffb390539d0e"

    time.sleep(1)
    response_get_queue = requests.get(queue_url,auth=authentication_tuple)
    print(response_get_queue.headers)
    s = str(response_get_queue.headers)

    s = s.replace("'", '"')
    js = json.loads(s)
    zip_url = js['Location']

    time.sleep(1)
    save_file_path = os.getcwd() + "/Confluence-space-export-" + key + ".xml.zip"
    print(save_file_path)
    time.sleep(10)
    download_url(url = zip_url, save_path = save_file_path)

# p = requests.get('http://localhost:1990/confluence/rest/confapi/1/backup/export/ds',auth=authentication_tuple)
# r = requests.get('http://localhost:1990/confluence/rest/confapi/1/backup/queue/babd669f-6eb9-421a-b22d-2dcd9bd9dd06',auth=('admin','admin'))
# q = requests.get('http://localhost:1990/confluence/download/temp/Confluence-space-export-121346-26.xml.zip',auth=('admin','admin'))
# file = open("./dumps.txt","w+")


# print(r.headers)
# print(r.ok)
# print(r)

# print(q.headers)
# print(q.ok)
# print(q)
#
# file.write(q.text)
#
# time.sleep(3)
#

#
# download_url()
