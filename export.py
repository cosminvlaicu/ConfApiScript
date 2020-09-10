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

def parse_json(headers):
    s = str(headers)
    s = s.replace("'", '"')
    return json.loads(s)

authentication_tuple = ('admin','admin')


base_url = sys.argv[1]
key_list = sys.argv[2].split(',')

custom_wait = 1
if len(sys.argv) > 3:
    custom_wait = float(sys.argv[3])

for key in key_list:
    request_page_url = base_url + "/rest/confapi/1/backup/export/" + key

    response_request_page = requests.get(request_page_url,auth=authentication_tuple)
    js = parse_json(response_request_page.headers)
    queue_url = js['Location']
    time.sleep(0.20*custom_wait)

    response_get_queue = requests.get(queue_url,auth=authentication_tuple)
    if not response_get_queue.ok:
        print("No task found for the given UUID")
        exit()

    js = parse_json(response_get_queue.headers)
    zip_url = js['Location']
    time.sleep(0.15*custom_wait)

    save_file_path = os.getcwd() + "/Confluence-space-export-" + key + ".xml.zip"
    time.sleep(0.05*custom_wait)
    download_url(url = zip_url, save_path = save_file_path)


