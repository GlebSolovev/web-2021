# web-2021
Prototype of **"One day - one happy person app"**.

To *run app* use:

```docker-compose -f karma_service/docker-compose.yml up```<br/>
```celery -A karma_service.celery_worker worker -l info -Q test-queue -c 1```
```python3 -m bank_service.main```<br/>
```python3 -m karma_service.main```<br/>
```python3 -m users_service.main```<br/>
```uvicorn app.main:app --reload```

via different terminal sessions in directory that contains app.

Then see Flower at: http://localhost:5555/<br/>
and RabbitMQ at: http://localhost:15672/

To *run autotests* use: ```python3 -m pytest --ignore=app/test/test_users_handler.py``` in the same directory.<br/>
For now ```app/test/test_users_handler.py``` can be used only manually, reloading all grpc services each test. 

See documentation about
* OpenAPI endpoints: http://127.0.0.1:8000/docs
* GraphiQL endpoint: http://127.0.0.1:8000/happy-persons-records

while running the app.
