import requests
import json
import time

#TODO: export endpoints to file/table/db

url = 'http://127.0.0.1:3000'
root = "/home/sasho_b/Coding/cob/user"
file_name = 'main.py'

def upload():
    endpoint = "/user/john_doe/project/myproject"
    r = None
    with open(root+"/"+file_name, 'rb') as file:
        files = {'upload': (file_name, file, 'text/plain')}
        r = requests.post(url + endpoint, files=files) # files= keyarg is specially turned into form-data
    
    # Print the response text
    print(r.text)

def run():
    endpoint = "/user/john_doe/project/myproject/run"
    r = requests.post(url + endpoint) # files= keyarg is specially turned into form-data
    print(r.text)
    pr = requests.get(url+endpoint+"?uuid="+r.json()["uuid"])
    while(pr.json().get('result') == None):
        pr = requests.get(url+endpoint+"?uuid="+r.json()["uuid"])
        time.sleep(0.5)
    print("Writing result")
    with open(root+"/result.txt", 'w+') as file:
        file.write(pr.text)
        print("Result in 'result.txt'")
        file.close()

def get():
    endpoint = "/user/john_doe/project/myproject/run"
    r = requests.get(url + endpoint)
    print(r.text)


if __name__ == "__main__":
    upload()
    run()

