from __future__ import annotations
import docker
import logging
from docker.errors import DockerException

log = logging.getLogger('Deploy service')


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
            log.warning(f'Error: {err}')
            return
        finally:
            self.client.containers.prune()

        log.info(f'Container {container_name} had been successfully deleted')

    def _deploy_new_container(self, image_name: str, container_name: str, ports: dict, build: bool) -> bool:
        try:
            if not build:
                log.info(f'Pull: {image_name}, Name: {container_name}')
                self.client.images.pull(image_name)

            log.info('Success')
            self._kill_container(container_name)
            log.info('Old container killed')
            self.client.containers.run(image=image_name, name=container_name, detach=True, ports=ports)
        except Exception as error:
            log.warning(f'Deploy {container_name} error: {error}')
            return False

        log.info(f'Container {container_name} deployd successfully')
        return True

    def _build_image(self, path: str, image_name: str, container_name: str, ports: dict, build: bool) -> bool:
        try:
            self.client.images.build(path=path, rm=True, tag=image_name)
            return self._deploy_new_container(container_name=container_name, image_name=image_name, ports=ports,
                                              build=build)
        except Exception as error:
            log.warning(f'Build {image_name} error: {error}')
            return False

    def start(self, image_name: str, container_name: str, path: str, ports: dict[str, int], build: bool) -> None:
        if build:
            success = self._build_image(container_name=container_name, image_name=image_name, ports=ports, path=path,
                                        build=build)
        else:
            success = self._deploy_new_container(image_name=image_name, container_name=container_name, ports=ports,
                                                 build=build)

        if not success:
            # TODO add send notifications
            pass
