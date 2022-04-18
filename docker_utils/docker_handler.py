from __future__ import annotations

import docker


class DockerHandler:
    def __init__(self) -> None:
        self.client = docker.from_env()

    def kill_container(self) -> DockerHandler:
        return self

    def build_image(self) -> DockerHandler:
        return self

    def run_image(self) -> DockerHandler:
        return self
