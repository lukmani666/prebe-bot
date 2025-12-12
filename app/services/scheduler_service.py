from datetime import datetime, timedelta
from app.services.followup_service import FollowupService
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
  """
  Lightweight scheduler for MVP: compute schedule times and call followup_service.
  Celery beat + tasks should be used for real scheduling.
  """
  def __init__(self):
    self.followup = FollowupService()
  
  def schedule_reminder(self, phone: str, when: datetime, payload: dict):
    """
    For MVP we send immediately if 'when' is in the past or soon.
    In production enqueue into Celery with eta=when.
    """
    now = datetime.utcnow()
    if when <= now:
      logger.info("Sending immediate reminder to %s", phone)
      return self.followup.send_followup(phone, payload)
    # TODO: enqueue into Celery with eta
    logger.info("Schedule reminder at %s for %s (not implemented, send immediately)", when, phone)
    return self.followup.send_followup(phone, payload)