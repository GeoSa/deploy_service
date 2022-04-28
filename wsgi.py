from app import app, AUTH_TOKEN
from logger import init_logger


if __name__ == '__main__':
    if AUTH_TOKEN is None:
        print('Need Auth Token')
        exit(1)

    init_logger('Deploy service')
    app.run(host='0.0.0.0', port=5000)
