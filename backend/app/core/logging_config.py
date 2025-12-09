import logging
import sys

def configure_logging():
  root = logging.getLogger()
  if not root.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
      "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
  root.setLevel(logging.INFO)

configure_logging()