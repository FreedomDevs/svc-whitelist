from datetime import datetime
import uuid


def success_response(data, message: str, code: str, trace_id: str | None):
    return {
        "data": data,
        "message": message,
        "meta": {
            "code": code,
            "traceId": trace_id or uuid.uuid4().hex,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }


def error_response(message: str, code: str, trace_id: str | None):
    return {
        "error": {
            "message": message,
            "code": code
        },
        "meta": {
            "traceId": trace_id or uuid.uuid4().hex,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }