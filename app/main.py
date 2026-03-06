from fastapi import FastAPI, Request
from app.schemas import WhitelistCreateRequest, WhitelistDeleteRequest
from app.responses import success_response, error_response
from app.db import SessionLocal
from app.models import Base, Whitelist
from app.enums import Codes
from sqlalchemy import text
from app.db import engine

app = FastAPI(title="svc-whitelist")
Base.metadata.create_all(bind=engine)


# вайтлист ендпоинты

@app.post("/whitelist", status_code=201)
def add_to_whitelist(req: WhitelistCreateRequest, request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    existing = db.query(Whitelist).filter(
        Whitelist.servername == req.servername,
        Whitelist.userid == req.userid
    ).first()

    if existing:
        return error_response(
            message="User already in whitelist",
            code=Codes.WHITELIST_ALREADY_EXISTS,
            trace_id=trace_id
        )

    user = Whitelist(
        servername=req.servername,
        userid=req.userid,
        username=req.username
    )

    db.add(user)
    db.commit()

    return success_response(
        data=req.dict(),
        message="User added to whitelist",
        code=Codes.WHITELIST_CREATED_OK,
        trace_id=trace_id
    )
@app.get("/whitelist/check")
def check_whitelist(request: Request, userid: str, servername: str | None = None):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    if servername:
        exists = db.query(Whitelist).filter(
            Whitelist.servername == servername,
            Whitelist.userid == userid
        ).first() is not None

        return success_response(
            data={"whitelisted": exists},
            message="Whitelist status checked",
            code=Codes.WHITELIST_CHECK_OK,
            trace_id=trace_id
        )

    rows = db.query(Whitelist).filter(
        Whitelist.userid == userid
    ).all()

    servers = [r.servername for r in rows]

    return success_response(
        data={
            "userid": userid,
            "servers": servers,
            "in_whitelist": bool(servers)
        },
        message="Whitelist servers fetched",
        code=Codes.WHITELIST_CHECK_OK,
        trace_id=trace_id
    )
@app.delete("/whitelist")
def remove_from_whitelist(req: WhitelistDeleteRequest, request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    user = db.query(Whitelist).filter(
        Whitelist.servername == req.servername,
        Whitelist.userid == req.userid
    ).first()

    if not user:
        return error_response(
            message="User not found in whitelist",
            code=Codes.WHITELIST_NOT_FOUND,
            trace_id=trace_id
        )

    db.delete(user)
    db.commit()

    return success_response(
        data=None,
        message="User removed from whitelist",
        code=Codes.WHITELIST_REMOVED_OK,
        trace_id=trace_id
    )




@app.get("/health")
def health(request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    details: dict[str, str] = {}
    ready = True

    # мемори
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        details["memory"] = "OK"
    except Exception as e:
        details["memory"] = f"ERROR: {str(e)}"
        ready = False

    # датабаза
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        details["database"] = "OK"
    except Exception as e:
        details["database"] = f"ERROR: {str(e)}"
        ready = False


    return success_response(
        data={
            "status": "UP" if ready else "ERROR",
            "ready": ready,
            "details": details
        },
        message="Service is healthy",
        code=Codes.HEALTH_OK,
        trace_id=trace_id
    )

@app.get("/live")
def live(request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    return success_response(
        data={"alive": True},
        message="svc-whitelist alive",
        code=Codes.LIVE_OK,
        trace_id=trace_id
    )
