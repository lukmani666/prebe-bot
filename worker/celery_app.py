from celery import Celery
from kombu import Exchange, Queue
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

app = Celery(
  "growthflow_worker",
  broker=CELERY_BROKER_URL,
  backend=CELERY_RESULT_BACKEND,
  include=[
    "worker.tasks.send_followup",
    "worker.tasks.train_next_buy_model",
    "worker.tasks.sync_predictions",
  ]
)

app.conf.task_queues = (
  Queue("followup_queue", Exchange("followup"), routing_key="followup.*"),
  Queue("training_queue", Exchange("training"), routing_key="training.*"),
  Queue("prediction_queue", Exchange("prediction"), routing_key="prediction.*"),
)

app.conf.task_default_exchange = "topic"
app.conf.result_expires = 3600
app.conf.task_time_limit = 300