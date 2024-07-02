import requests
import multipart

url = 'http://127.0.0.1:3000'
endpoint = "/upload_code/john_doe"
file_name = 'my_file.txt'
r = None

if __name__ == "__main__":
    with open(file_name, 'rb') as file:
        files = {'upload': (file_name, file, 'text/plain')}
        
        r = requests.post(url + endpoint, files=files) # files= keyarg is specially turned into form-data
    
    # Print the response text
    print(r.text)
