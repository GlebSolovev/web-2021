# web-2021
Prototype of **"One day - one happy person app"**.

To *run app* use:

```python3 -m bank_service.main```<br/>
```python3 -m karma_service.main```<br/>
```python3 -m users_service.main```<br/>
```uvicorn app.main:app --reload```

via different terminal sessions in directory that contains app.

See Flower at: http://localhost:5555/
See RabbitMQ at: http://localhost:15672/

To *run autotests* use: ```python3 -m pytest --ignore=app/test/test_users_handler.py``` in the same directory.<br/>
For now ```app/test/test_users_handler.py``` can be used only manually, reloading all grpc services each test. 

See documentation about
* OpenAPI endpoints: http://127.0.0.1:8000/docs
* GraphiQL endpoint: http://127.0.0.1:8000/happy-persons-records

while running the app.
