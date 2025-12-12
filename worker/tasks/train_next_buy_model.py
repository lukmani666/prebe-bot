from worker.celery_app import app
from backend.ml.training.next_buy_trainer import train_next_buy_model

@app.task(queue="training_queue", routing_key="training.model.next_buy")
def retrain_next_buy_model():
    """Rebuild Next-Buy Prediction Model."""
    model_path = train_next_buy_model()
    return {"message": "model retrained", "path": model_path}
