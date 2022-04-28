from app import app, AUTH_TOKEN
from logger import init_logger


if __name__ == '__main__':
    print(AUTH_TOKEN)
    init_logger('Deploy service')
    app.run(host='0.0.0.0', port=5000)
