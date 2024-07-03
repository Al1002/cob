This file is a technical introduction to COB.

1. Components
The app is separated into 2 parts - the thing that runs containers and the thing that handles web requests - `build_container.py` and `fast.py` respectively

1.a `fast.py`
`fast.py` is the FastAPI app, containing the endpoints. Its ran with `fastapi [run/dev]` for production/dev server.
The endpoints are decorated as per FastAPI with @app.[request type]("endpoint",...).
The users are simply directories.

Endpoints expect 3 things - headers, querry parameters, and body. (Explained well in the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/))
Results are usually in a json/application format.


GET /{user}/code - returns a list of user files

POST /{user}/code - expects a file attachment called "upload", with a python script file (must end with .py), and puts it in the user folder.

POST /{user}/run/{filename} - executes the apropriate file from the user's folder and returns
a response with the result (the stdout, i.e. printed text) using `build_container.py`

1.b `build_container.py`
Manages docker containers and images. Requires the python docker api ([docs here](https://docker-py.readthedocs.io/en/stable/)).
Whenever a script needs to be ran with `run_code()`, it is first coppied into the `docker/python` folder.
`dockerfile_template`'s placeholder names are replaced with the name of the script to be run.
This filled out template is then coppied into `docker/python` as well.
Finaly, using the docker api, an image is assembled, a container is made from that image, and its ran.
The image and container are deleted and the stdout (i.e. where print() writes to) from the container is returned. 

Adendum:

In future, the results will instead be saved to a DB rather than having to wait for the HTTP response.

