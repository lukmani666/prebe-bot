from worker.celery_app import app
from backend.app.services.followup_service import FollowupService

@app.task(queue="followup_queue", routing_key="followup.trigger")
def send_followup_message(customer_id: int):
  """Trigger automated follow-up workflow."""
  followup = FollowupService()
  followup.process_followup(customer_id)
  return {"status": "success", "customer_id": customer_id}