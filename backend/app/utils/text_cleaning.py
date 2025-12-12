import re

def clean_text(s: str) -> str:
  if not s:
    return ""
  s = s.strip()
  s = re.sub(r"\s+", " ", s)
  return s