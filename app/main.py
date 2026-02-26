from fastapi import FastAPI, Request
from app.schemas import WhitelistCreateRequest, WhitelistDeleteRequest
from app.responses import success_response, error_response
from app.storage import whitelist
from app.enums import Codes

app = FastAPI(title="svc-whitelist")


# вайтлист ендпоинты

@app.post("/v1/whitelist", status_code=201)
def add_to_whitelist(req: WhitelistCreateRequest, request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    server = whitelist.setdefault(req.servername, {})

    if req.userid in server:
        return error_response(
            message="User already in whitelist",
            code=Codes.WHITELIST_ALREADY_EXISTS,
            trace_id=trace_id
        )

    server[req.userid] = req.username

    return success_response(
        data={
            "servername": req.servername,
            "userid": req.userid,
            "username": req.username
        },
        message="User added to whitelist",
        code=Codes.WHITELIST_CREATED_OK,
        trace_id=trace_id
    )


@app.get("/v1/whitelist/check")
def check_whitelist(request: Request, userid: str, servername: str | None = None):
    trace_id = request.headers.get("X-Trace-Id")

    # есть ли пользователь на конкретном сервере
    if servername:
        return success_response(
            data={"whitelisted": userid in whitelist.get(servername, {})},
            message="Whitelist status checked",
            code=Codes.WHITELIST_CHECK_OK,
            trace_id=trace_id
        )

    # на каких серверах пользователь есть
    servers = [
        server for server, users in whitelist.items()
        if userid in users
    ]

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


@app.delete("/v1/whitelist")
def remove_from_whitelist(req: WhitelistDeleteRequest, request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    server = whitelist.get(req.servername)

    if not server or req.userid not in server:
        return error_response(
            message="User not found in whitelist",
            code=Codes.WHITELIST_NOT_FOUND,
            trace_id=trace_id
        )

    del server[req.userid]

    if not server:
        del whitelist[req.servername]

    return success_response(
        data=None,
        message="User removed from whitelist",
        code=Codes.WHITELIST_REMOVED_OK,
        trace_id=trace_id
    )


# системные ендпоинты

@app.get("/health")
def health(request: Request):
    trace_id = request.headers.get("X-Trace-Id")

    return success_response(
        data={
            "status": "UP",
            "ready": True,
            "details": {
                "memory": "OK"
            }
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