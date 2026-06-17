from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Depends
from starlette import status
from svcLibs.codes import HealthOK, LiveOK

from app.schemas import WhitelistCreateRequest, WhitelistDeleteRequest, UserBody
from app.db import SessionLocal
from app.models import Base, Whitelist
from app.enums import *
from sqlalchemy import text
from app.db import engine
from fastapi import FastAPI, Request, Header

from svcLibs.responses import success_response, error_response
from svcLibs.middleware import register_errors_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="svc-whitelist")
register_errors_handlers(app)

async def get_server_name(
        request: Request,
        eauth_type: Optional[str] = Header(None, alias="eauth-type"),
        eauth_server_name: Optional[str] = Header(None, alias="eauth-server-name"),
) -> str:
    if not eauth_type or eauth_type == "user":
        # Если user — читаем имя сервера из Body.
        # Так как нам нужно прочитать JSON, используем request.json()
        try:
            body_data = await request.json()
            # Валидируем данные через Pydantic-модель
            user_data = UserBody(**body_data)
            return user_data.server_name
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Неверный формат Body. Ожидалось поле 'server_name'."
            )

    elif eauth_type == "server":
        # Если server — проверяем заголовок "eauth"
        if not eauth_server_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Для eauth-type='server' необходим заголовок 'eauth'"
            )
        return eauth_server_name

    else:
        # Если передан неизвестный тип авторизации
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неподдерживаемый eauth-type. Допустимы 'user' или 'server'."
        )
# вайтлист ендпоинты

@app.post("/whitelist", status_code=201)
def add_to_whitelist(
    req: WhitelistCreateRequest,
    request: Request,
    server_name: str = Depends(get_server_name),
):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    existing = db.query(Whitelist).filter(
        Whitelist.servername == server_name,
        Whitelist.userid == req.userid
    ).first()


    if existing:
        return error_response(
            WhitelistAlreadyExists(),
            trace_id
        )

    user = Whitelist(
        servername=server_name,
        userid=req.userid
    )

    db.add(user)
    db.commit()

    return success_response(
        {
            "servername": server_name,
            **req.dict()
        },
        WhitelistCreatedOk(),
        trace_id
    )

from fastapi import Header

@app.get("/whitelist/check")
def check_whitelist(
    request: Request,
    userid: str,
    server_name: str = Depends(get_server_name),
):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    if server_name:
        exists = db.query(Whitelist).filter(
            Whitelist.servername == server_name,
            Whitelist.userid == userid
        ).first() is not None

        return success_response(
            {
                "in_whitelist": exists
            },
            WhitelistCheckOk(),
            trace_id
        )


    rows = db.query(Whitelist).filter(
        Whitelist.userid == userid
    ).all()

    servers = [r.servername for r in rows]

    return success_response(
        {
            "userid": userid,
            "servers": servers,
            "in_whitelist": bool(servers)
        },
        WhitelistCheckOk(),
        trace_id
    )



@app.delete("/whitelist")
def remove_from_whitelist(
    req: WhitelistDeleteRequest,
    request: Request,
    server_name = Depends(get_server_name),
):
    trace_id = request.headers.get("X-Trace-Id")

    db = SessionLocal()

    user = db.query(Whitelist).filter(
        Whitelist.servername == server_name,
        Whitelist.userid == req.userid
    ).first()

    if not user:
        return error_response(
            WhitelistNotFound(),
            trace_id
        )

    db.delete(user)
    db.commit()

    return success_response(
        None,
        WhitelistRemovedOk(),
        trace_id
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
        {
            "status": "UP" if ready else "ERROR",
            "ready": ready,
            "details": details
        },
        HealthOK(),
        trace_id
    )

@app.get("/live")
def live(request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    return success_response(
        {"alive": True},
        LiveOK(),
        trace_id
    )
