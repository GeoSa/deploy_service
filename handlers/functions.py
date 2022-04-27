def process_request(request_data: dict) -> bool:
    owner = request_data.get('owner')
    repository = request_data.get('repository')
    tag = request_data.get('tag')
    ports = request_data.get('ports')
    path = request_data.get('path')
    build = request_data.get('build')

    if not build and (not owner or not repository or not tag or not ports):
        return False

    if build and (not path or not tag or not ports):
        return False

    return True


def get_image_name(owner: str = None, repository: str = None, tag: str = None) -> [str, str]:
    if tag and (not owner or not repository):
        return tag, tag

    if tag and owner and repository:
        return f'{owner}/{repository}:{tag}', repository

    return '', ''
