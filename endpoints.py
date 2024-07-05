# pluralize all endpoints

@app.get("/")
# wellcome msg

@app.get("/user")
#login, n/a

@app.post("/user")
#user creation request

@app.post("/user/{user}/project")
#project creation request

@app.get("/user/{user}/project")
#list of user projects

@app.post("/user/{user}/project/{project}")
#project upload

@app.get("/user/{user}/project/{project}")
#project state

@app.get("/user/{user}/project/{project}")
#project state

@app.post("/user/{user}/project/{project}/run")
#start the project

@app.get("/user/{user}/project/{project}/run")
#runing state; result

#structure:
# users/john/projects/greatestProject/hello.py
# mongo user schema:
#{
    # "user": WhoAmI,
    # "project": greatestProject
    # "project_type": Enum[python, java, go]
    # "entry_point": hello.py
    # ?"image_id":
#}
# mongo result schema:
#{
    # "project": greatestProject
    # "timestamp": 06:09:42 
    # "log": "8%2(2+2)=16"
    # ""
#}
#
