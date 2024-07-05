import docker

from pathlib import Path
from shutil import copyfile
from threading import Thread

ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")

CLIENT = docker.from_env()

# cass which runs containers and saves their results to MongoDB
# takes a template Dockerfile and fills it out
def fillout_template(
    entry_file: Path, 
    source_dir: Path,
    output_dir: Path,
    docker_template: Path = DOCKER_TEMPLATE
    ) -> None:
    template = ''
    with open(docker_template, 'r') as file:
        template = file.read()
        template = template.replace('{source_file}', entry_file.name)
    with open(Path(output_dir,"Dockerfile"), "w+") as save_to:
        save_to.write(template)

# prepares the image build dir
def prepare_build_directory(
    entry_file: Path,
    source_dir: Path,
    build_dir: Path
    ) -> None:
    fillout_template(entry_file, source_dir, build_dir)
    copyfile(entry_file, Path(build_dir,entry_file.name))

# s.e.
def build_image(
    entry_file: Path,
    source_dir: Path,
    build_dir: Path
    ):
    prepare_build_directory(entry_file, source_dir, build_dir)
    image = CLIENT.images.build(path=str(Path(ROOT, "python")), rm=True)[0] # rm=True OR IT BREAKS!
    return image

# s.e.
def build_container( image):
    return CLIENT.containers.create(image.id)

# starts a container, wairs for it to finish and returns its stdout as a string
def run_container( container):
    container.start()
    container.wait()
    return container.logs().decode()

# configures a project and executes it, then cleans up
def run_project(
    entry_file: Path,
    source_dir: Path,
    build_dir: Path = Path(ROOT,"python"),
    ):
    image = build_image(entry_file, source_dir, build_dir)
    container = build_container(image)
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