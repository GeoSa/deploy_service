from __future__ import annotations
import docker
from docker.errors import DockerException


class DockerHandler:
    def __init__(self) -> None:
        try:
            self.client = docker.from_env()
        except DockerException:
            raise Exception("Docker doesn't install")

    def _kill_container(self, container_name: str) -> None:
        try:
            container = self.client.containers.get(container_name)
            container.kill()
        except Exception as err:
            print(f'Error: {err}')
            return
        finally:
            self.client.containers.prune()

        print(f'Container {container_name} had been successfully deleted')

    def _deploy_new_container(self, image_name: str, container_name: str, ports: dict) -> bool:
        try:
            print(f'Pull: {image_name}, Name: {container_name}')
            self.client.images.pull(image_name)
            print(f'Success')
            self._kill_container(container_name)
            print(f'Old container killed')
            self.client.containers.run(image=image_name, name=container_name, detach=True, ports=ports)
        except Exception as error:
            print(f'Deploy {container_name} error: {error}')
            return False

        print(f'Container {container_name} deployd successfully')
        return True

    def _build_image(self, path: str, image_name: str, container_name: str, ports: dict) -> bool:
        try:
            self.client.images.build(path=path, rm=True, tag=image_name)
            return self._deploy_new_container(container_name=container_name, image_name=image_name, ports=ports)
        except Exception as error:
            print(f'Build {image_name} error: {error}')
            return False

    def start(self, image_name: str, container_name: str, path: str, ports: dict[str, int], build: bool) -> None:
        if build:
            success = self._build_image(container_name=container_name, image_name=image_name, ports=ports, path=path)
        else:
            success = self._deploy_new_container(image_name=image_name, container_name=container_name, ports=ports)

        if not success:
            # TODO add send notifications
            pass


