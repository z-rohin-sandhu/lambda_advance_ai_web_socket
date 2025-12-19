import json
from src.utils.logging import log

def json_dumps(data):
    try:
        return json.dumps(data)
    except Exception as exc:
        log("json_dumps failed", level="ERROR", error=str(exc))
        return ""

def json_loads(data):
    try:
        return json.loads(data)
    except Exception as exc:
        log("json_loads failed", level="ERROR", error=str(exc))
        return {}
