from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Whitelist(Base):
    __tablename__ = "whitelist"

    servername = Column(String, primary_key=True)
    userid = Column(String, primary_key=True)
    username = Column(String)
