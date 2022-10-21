#!/bin/bash

export AWS_ACCESS_KEY_ID='13870'
export AWS_SECRET_ACCESS_KEY='13870'
export AWS_DEFAULT_REGION='us-east-1'
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000