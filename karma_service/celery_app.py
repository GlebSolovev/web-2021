from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://:password123@localhost:6379/0",
    broker="amqp://user:bitnami@localhost:5672//"
)

celery_app.conf.task_routes = {
    "karma_service.celery_worker.calculate_stat": "test-queue"}
celery_app.conf.update(task_track_started=True)
