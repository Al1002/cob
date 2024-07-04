import docker

from pathlib import Path
from shutil import copyfile
from threading import Thread
import uuid

import db_interface

ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")

CLIENT = docker.from_env()

# class which runs containers and saves their results to MongoDB
class ContainerManager:
    # takes a template Dockerfile and fills it out
    def fillout_template(self,
        entry_file: Path, 
        source_dir: Path,
        output_dir: Path,
        docker_template: Path = DOCKER_TEMPLATE
        ) -> None:
        template = ''
        with open(docker_template, 'r') as file:
            template = file.read()
            template = template.replace('{source_file}', entry_file.name)
        with open(output_dir+"Dockerfile","w+") as save_to:
            save_to.write(template)
    
    # prepares the image build dir
    def prepare_build_directory(self,
        entry_file: Path,
        source_dir: Path,
        build_dir: Path
        ) -> None:
        self.fillout_template(entry_file, source_dir, build_dir)
        copyfile(entry_file, build_dir + entry_file.name)

    # s.e.
    def build_image(self,
        entry_file: Path,
        source_dir: Path,
        build_dir: Path
        ):
        self.prepare_build_directory(entry_file, source_dir, build_dir)
        image = CLIENT.images.build(path=str(ROOT + "python"), rm=True)[0] # rm=True OR IT BREAKS!
        return image

    # s.e.
    def build_container(self, image):
        return CLIENT.containers.create(image.id)

    # starts a container, wairs for it to finish and returns its stdout as a string
    def run_container(self, container):
        container.start()
        container.wait()
        return container.logs().decode()

    # configures a project and executes it, then cleans up
    def run_project(self,
        entry_file: Path,
        source_dir: Path,
        build_dir: Path = ROOT+"python",
        ):
        image = self.build_image(entry_file, source_dir, build_dir)
        container = self.build_container(image)
        result = self.run_container(container)
        container.remove(force=True)
        image.remove(force=True)
        return result
    
    # runs a project and saves its output to a database, along with an identifier for retrieval
    def container_output_to_db(self, entry_file: Path, id: uuid.UUID) -> None:
        result = self.run_project(entry_file, source_dir=None)
        db_interface.save_results({'uuid': id, "result": result})

    # runs a project in a separate thread. returns an identifier for retrieval
    def thread_project(self, source_file: Path) -> uuid.UUID:
        id = uuid.uuid4()
        thread = Thread(target=self.container_output_to_db, args=[self, source_file, id])
        thread.daemon = False
        thread.start()
        return id

if __name__ == "__main__":
    source_dir = Path("/home/sasho_b/Coding/cob/user")
    entry_point = source_dir + "hello.py"
    result = ContainerManager.run_project(entry_point, source_dir)
    print(result)
    print("Done")