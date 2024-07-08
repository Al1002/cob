import docker

from pathlib import Path

ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")

CLIENT = docker.from_env()

class Project:
    entry_file: str
    source_dir: str
    build_dir: str

# cass which runs containers and saves their results to MongoDB
# takes a template Dockerfile and fills it out
def fillout_template(entry_file: Path, source_dir: Path,output_dir: Path,docker_template: Path = DOCKER_TEMPLATE) -> None:
    template = ''
    with open(docker_template, 'r') as file:
        template = file.read()
        template = template.replace('{entry_file}', entry_file.name)
    with open(Path(output_dir,"Dockerfile"), "w+") as save_to:
        save_to.write(template)

# starts a container, wairs for it to finish and returns its stdout as a string
def run_container(container):
    container.start()
    container.wait()
    return container.logs().decode()

# configures a project and executes it, then cleans up
def run_project(entry_file: Path,source_dir: Path,build_dir: Path | None = None,):
    if build_dir == None:
        build_dir = source_dir
    fillout_template(entry_file, source_dir, build_dir)
    image = CLIENT.images.build(path=str(build_dir), rm=True)[0] # rm=True OR IT BREAKS!
    container = CLIENT.containers.create(image.id)
    result = run_container(container)
    container.remove(force=True)
    image.remove(force=True)
    return result

if __name__ == "__main__":
    source_dir = Path("/home/sasho_b/Coding/cob/user")
    entry_point = Path(source_dir, "hello.py")
    result = run_project(entry_point, source_dir)
    print(result)
    print("Done")

