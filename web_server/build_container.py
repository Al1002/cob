import docker
from pathlib import Path
from shutil import copyfile

root = Path("/home/sasho_b/Coding/cob/docker")
template_file = Path(root, "dockerfile_template")

client = docker.from_env()

def fillout_template(source_file: Path, template_file: Path, output_dir: Path):
    template = open(template_file).read()
    template = template.replace('{source_file}', source_file.name)
    save_to = open(Path(output_dir, "Dockerfile"),"w+")
    save_to.write(template)
    save_to.close()

# takes a template docker file, a source, and puts them into a dir where an image is built
def build_image(source_file: Path, template_file: Path, build_dir: Path):
    fillout_template(source_file, template_file, build_dir)
    copyfile(source_file, Path(build_dir, source_file.name))
    return client.images.build(path=str(Path(root,"python")), rm=True)[0] # rm=True OR IT BREAKS!

def build_container(image):
    return client.containers.create(image.id)

def run_container(container):
    container.start()
    container.wait()
    return container.logs().decode()


def run_code(source_file: Path):
    build_dir = Path(root, "python")
    image = build_image(source_file, template_file, build_dir)
    container = build_container(image)
    result = run_container(container)
    container.remove(force=True)
    image.remove(force=True)
    return result

if __name__ == "__main__":
    print(run_code(Path("/home/sasho_b/Coding/cob/user", "hello.py")))
    print("Done")