import requests
import multipart

url = 'http://127.0.0.1:3000'
file_name = 'my_file.txt'

def upload():
    endpoint = "/john_doe/code"
    r = None
    with open(file_name, 'rb') as file:
        files = {'upload': (file_name, file, 'text/plain')}
        
    r = requests.post(url + endpoint, files=files) # files= keyarg is specially turned into form-data
    
    # Print the response text
    print(r.text)

def get():
    endpoint = "/john_doe/code"
    r = requests.get(url + endpoint)
    print(r.text)

if __name__ == "__main__":
    get()