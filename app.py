import json
import os
from flask import Flask, request, jsonify, Response
from python_on_whales import DockerClient

from docker_utils import docker_handler
from handlers import process_request, get_image_name
from logger import init_logger

app = Flask(__name__)
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
init_logger('deploy_service')


@app.route('/', methods=['POST'])
def process_webhook() -> tuple[Response, int]:
    if request.headers.get('Authorization', '') != AUTH_TOKEN:
        return jsonify({'message': 'Bad token'}), 401

    try:
        request_data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'message': 'Bad request'}), 401

    if not process_request(request_data):
        return jsonify({'message': 'Bad request'}), 401

    owner = request_data.get('owner')
    repository = request_data.get('repository')
    tag = request_data.get('tag')
    ports = request_data.get('ports')
    path = request_data.get('path')
    build = request_data.get('build')

    image_name, container_name = get_image_name(owner=owner, repository=repository, tag=tag)
    docker_handler.start(image_name=image_name, container_name=container_name, ports=ports, path=path, build=build)
    return jsonify({'message': 'Deploy complete'}), 200


@app.route('/compose', methods=['POST'])
def process_compose_webhook() -> tuple[Response, int]:
    if request.headers.get('Authorization', '') != AUTH_TOKEN:
        return jsonify({'message': 'Bad token'}), 401

    try:
        request_data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'message': 'Bad request'}), 401

    path = request_data.get('path')
    file = request_data.get('file')

    if path is None or file is None:
        return jsonify({'message': 'Bad request'}), 401

    full_filename = os.path.join(path, file)
    try:
        docker = DockerClient(compose_files=[full_filename])
        docker.compose.build()
        docker.compose.up(detach=True)
        return jsonify({'message': 'Deploy complete'}), 200
    except Exception:
        return jsonify({'message': 'Deploy error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
