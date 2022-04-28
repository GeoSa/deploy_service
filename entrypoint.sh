#!/bin/bash
mkdir logs
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --reload --timeout 600
