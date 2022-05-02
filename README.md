# Deploy service
## Deployment:

### Create virtual environment
python -m venv venv

### Activate virtual environment
#### Linux
source venv/bin/activate
#### Windows
venv/Scripts/activate.bat

### Install dependencies
pip install -r requirements.txt

### Run locally
#### Via gunicorn
gunicorn app:app --bind 0.0.0.0:8081 --reload  
use --daemon flag optionally to run process as a daemon
#### Via python
python app.py