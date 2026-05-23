from pydantic import BaseModel


class WhitelistCreateRequest(BaseModel):
    userid: str
    username: str


class WhitelistDeleteRequest(BaseModel):
    userid: str

class UserBody(BaseModel):
    server_name: str
