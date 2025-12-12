from worker.celery_app import app
from backend.app.services.prediction_service import PredictionService

@app.task(queue="prediction_queue", routing_key="prediction.sync")
def sync_prediction_scores():
    """Generate and store churn/next-buy predictions."""
    service = PredictionService()
    count = service.recompute_all_predictions()
    return {"synced_predictions": count}
