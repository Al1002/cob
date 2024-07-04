import requests
import json
import time

url = 'http://127.0.0.1:3000'
root = "/home/sasho_b/Coding/cob/user"
file_name = 'hello.py'

def upload():
    endpoint = "/john_doe/code"
    r = None
    with open(root+"/"+file_name, 'rb') as file:
        files = {'upload': (file_name, file, 'text/plain')}
        r = requests.post(url + endpoint, files=files) # files= keyarg is specially turned into form-data
    
    # Print the response text
    print(r.text)

def run():
    endpoint = "/john_doe/run/hello.py"
    r = requests.post(url + endpoint) # files= keyarg is specially turned into form-data
    print(r.text)
    pr = requests.get(url+"/john_doe/result/"+r.json()["uuid"])
    while(pr.json().get('result') == None):
        pr = requests.get(url+"/john_doe/result/"+r.json()["uuid"])
        time.sleep(5)
    print(pr.json()["result"])

def get():
    endpoint = "/john_doe/code"
    r = requests.get(url + endpoint)
    print(r.text)

if __name__ == "__main__":
    upload()
    get()
    run()