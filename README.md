# COB
### What is COB?

COB is a web service which accepts user code, prepares it, and runs it in an isolated environment.

### What is COB made out of?

COB is comprised of a web server and a script to run containers.

The web server is written in python with FastAPI.

It depends on docker's python api.

### How do i run it?

1. Download the repo using
```git clone git@github.com:Al1002/cob.git```

2. Download the relevant dependencies with pip
```pip install fastapi```
```pip install docker```
