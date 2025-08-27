# API to GPIO

## Install
- mkdir Someting
- cd Someting
- git pull https://github.com/danlarsson/API-to-LED.git

- cd API-to-LED
- python -m venv venv
- pip install -r requirement.txt


## Run with
- source venv/bin/activate
- uvicorn main:app --host 0.0.0.0 --port 8073


## Test 
- http://serverip:8073
- http://serverip:8073/docs

