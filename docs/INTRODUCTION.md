This file is a technical introduction to COB - a web service which executes user code

As of 08.07.2024, this file is out of date.

1. Components
The app is separated into 2 parts - the thing that handles web requests and the thing that runs containers - `fast.py` and `build_container.py` respectively

1.a `fast.py`
`fast.py` is the FastAPI python app, containing the endpoints. Its ran with `fastapi [run/dev]` for production/dev server.
The endpoints are decorated as per FastAPI with @app.{request type}("endpoint",...).
The users are simply directories in `web_server/users`.

Endpoints expect 3 things - headers, querry parameters, and body. (Explained well in the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/))
Results are usually in a json/application format.

The endpoints are listed in the automatic swagger documentation provided by FastAPI. 

Generaly, the units the app deals with are users, projects, and files. 

1.b `build_container.py`
Manages docker containers and images. Requires the python docker api ([docs here](https://docker-py.readthedocs.io/en/stable/)).
Whenever a script needs to be ran with `run_code()`, it is first coppied into the `docker/python` folder.
`dockerfile_template`'s placeholder names are replaced with the name of the script to be run.
This filled out template is then coppied into `docker/python` as well.
Finaly, using the docker api, an image is assembled, a container is made from that image, and its ran.
The image and container are deleted and the stdout (i.e. where print() writes to) from the container is returned. 

2. User
Currently there is no user interface. There exists a folder `user` which contains example python code to make requests and test the main app.

