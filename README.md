# COB
### What is COB?

COB is a web service which accepts user code, prepares it, and runs it in an isolated environment.

### What is COB comprised of?

COB is comprised of a web server and a script to run containers.

The web server is written in python with FastAPI.

It depends on docker's python api.

### How do I run it?

1. Download the repo using
```git clone git@github.com:Al1002/cob.git```

2. Download the relevant dependencies with pip 
```pip install fastapi```
```pip install docker```
(you could put them in a venv if needed)

3. Run the web server using
```fastapi run web_server/fast.py```
Note: the default port for the server is 8000, if its occupied, use the ```--port XXXX``` flag to change it

4. Checkout the ```user/main.py``` script for example usage

### How can I contribute?

Contact me at aleksandriliev05@gmail.com if you wish to contribute, give suggestions, new ideas, or aid the project in any way.



