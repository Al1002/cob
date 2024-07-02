import docker

template_file = "dockerfile_template"

def fillout_template(source_file: str):
    template = open(template_file).read()
    template = template.replace('{source_file}', source_file)
    return template

def build_container(source_file: str):
    commands = fillout_template(source_file)
    client = docker.from_env()
    container = client.containers.create("python:latest", command=commands)

