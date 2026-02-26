from pydantic import BaseModel


class WhitelistCreateRequest(BaseModel):
    servername: str
    userid: str
    username: str


class WhitelistDeleteRequest(BaseModel):
    servername: str
    userid: str