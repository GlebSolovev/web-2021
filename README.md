# web-2021
Prototype of **"One day - one happy person app"**.

To *run app* use: ```uvicorn app.main:app --reload``` in directory that contains app.<br/>
To *run autotests* use: ```python3 -m pytest ./``` in the same directory.<br/>
To *run load locust test* use: ```locust -H http://127.0.0.1:8000 -f app/test/locustfile.py``` in the same directory.
