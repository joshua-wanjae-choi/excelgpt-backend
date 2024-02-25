from celery import Celery

app = Celery(
    "tasks", broker="pyamqp://guest@queue//", backend="rpc://", include=["proj.tasks"]
)
