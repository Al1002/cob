import docker
from pathlib import Path
from shutil import copyfile

root = Path("/home/sasho_b/Coding/cob/docker")
template_file = Path(root, "dockerfile_template")

client = docker.from_env()

def fillout_template(source_file: Path, template_file: Path, output_dir: Path):
    template = open(template_file).read()
    template = template.replace('{source_file}', source_file.name)
    open(Path(output_dir, "Dockerfile"),"w+").write(template)

# takes a template docker file, a source, and puts them into a dir where an image is built
def build_image(source_file: Path, template_file: Path, build_dir: Path):
    fillout_template(source_file, template_file, build_dir)
    copyfile(source_file, Path(build_dir, source_file.name))
    return client.images.build(path=str(Path(root,"python")))[0]

def remove_image(image_id: str):
    client.images.remove(image=image_id)

def run_container(image_id: str):
    container = client.containers.create(image_id)
    container.start()
    container.wait()
    result = container.logs().decode()
    container.remove()
    return result

def run_code(source_file: Path):
    build_dir = Path(root, "python")
    image = build_image(source_file, template_file, build_dir)
    result = run_container(image.id)
    remove_image(image.id)
    print(result)

if __name__ == "__main__":
    run_code(Path(root, "hello.py"))